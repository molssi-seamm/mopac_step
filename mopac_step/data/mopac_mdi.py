#!/usr/bin/env python3
"""
mopac_mdi.py -- MDI engine wrapping MOPAC via the mopactools Python API.

Unlike MOPAC's native Fortran MDI engine, this script needs no .mop input
file and no MPI-enabled MOPAC build: mopactools loads the plain libmopac
shared library directly, and all structural information (atom count,
elements, coordinates, cell) is obtained entirely from the MDI handshake
with the driver. Charge and spin are supplied via CLI defaults, optionally
overridden by >TOTCHARGE / >ELEC_MULT if the driver sends them (LAMMPS's
fix mdi/qm currently does not, as of the version tested this week).

Known issue carried over from MOPAC's native MDI engine, addressed here
by construction: MOPAC's stress tensor (calculate_voigt(), reached via
compfg.F90) is only populated when ALL lattice vectors are flagged
"movable" -- this script always sets nlattice_move = nlattice for exactly
this reason, mirroring the Tv "+1" workaround used for the native engine.
Confirmed working empirically via in.mopac_stress_check.

Sign conventions confirmed from the mopactools docstrings and this week's
native-engine validation:
    coord_deriv : dE/dx in kcal/(mol*Angstrom) -- force = -coord_deriv
    stress      : Voigt (xx,yy,zz,yz,xz,xy), GPa, tensile positive
                  (MOPAC convention) -- negate for MDI/LAMMPS (compressive
                  positive), exactly as established for the native engine.

MOZYME (--mozyme) is currently unreliable for periodic liquid MD: even
with --mozyme-restart-every 1 (a fresh Lewis-structure/LMO build every
single step, no state reuse at all), the bonding-analysis heuristic can
still occasionally mis-assign a transient hydrogen-bond contact as
covalent, producing a Lewis structure that doesn't balance to the
declared total charge ("Unit cell has a charge" / "ERROR DETECTED IN
SUBROUTINE CHECK"). This is a known open question for the MOPAC
developers, not something this script can paper over -- use the
conventional solver (the default, no --mozyme) for periodic liquid MD
until/unless that's resolved upstream.

Usage -- TCP mode (two terminals, simplest for testing):
    Terminal 1:
        python mopac_mdi.py \\
            -mdi "-role ENGINE -name MOPAC -method TCP -port 8021 \\
            -hostname localhost" --method PM6-ORG --charge 0 --multiplicity 1

    Terminal 2:
        mpirun -np 1 lmp -in in.mopac_nvt \\
            -mdi "-role DRIVER -name LAMMPS -method TCP -port 8021"

No --structure or --elements argument is needed if the LAMMPS fix mdi/qm
line uses the "elements" keyword (e.g. "elements C O H H") -- LAMMPS then
sends atomic numbers directly via >ELEMENTS. --elements is only needed as
a fallback if the driver instead sends LAMMPS atom types via >TYPES.

Dependencies:
    conda install -c conda-forge mopactools pymdi seamm_util
    (no MPI requirement on this side when using -method TCP)

Logging: three levels, set via --log-level.
    DEBUG   -- every MDI command received, plus per-call raw energy/stress
    INFO    -- lifecycle events, per-call timing, MOZYME restarts (default)
    WARNING -- only warnings and errors (quietest)
"""

# Pin MOPAC (and the BLAS/LAPACK it calls) to a single thread. MOPAC gets little
# benefit from threading on these small semiempirical SCFs, and an MDI driver
# typically issues many calls back-to-back, so multiple threads only
# oversubscribe the cores. Unlike the normal MOPAC step -- which launches MOPAC
# with an explicit OMP_NUM_THREADS -- this engine is spawned by the MDI driver
# with an inherited environment, so nothing else caps the thread count. Set the
# caps here, before numpy (and hence any MKL/OpenBLAS runtime) is imported, or
# the thread pool is already sized and the setting is ignored. `setdefault`
# leaves an explicitly-set environment override in place.
import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import argparse  # noqa: E402
import logging  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402

import numpy as np  # noqa: E402

from seamm_util import Q_  # noqa: E402

# mpi4py only needed for -method MPI; harmless if unused for TCP.
try:
    from mpi4py import MPI  # noqa: E402, F401
except ImportError:
    pass

logger = logging.getLogger("mopac-mdi")

# ---------------------------------------------------------------------------
# Unit conversion factors via seamm_util's Q_ (pint Quantity, pre-configured
# exactly as the rest of SEAMM uses it -- e.g. gaussian_step, thermomechanical_step
# both use Q_(value, "hartree").m_as(...)-style calls) rather than a bare
# pint.UnitRegistry() or hardwired CODATA constants. Computed once at import.
# ---------------------------------------------------------------------------

ANG_PER_BOHR = Q_(1.0, "bohr").m_as("angstrom")
BOHR_PER_ANG = Q_(1.0, "angstrom").m_as("bohr")
HARTREE_PER_KCALMOL = Q_(1.0, "kcal/mol").m_as("hartree")
GPA_PER_HARTREE_BOHR3 = Q_(1.0, "hartree/bohr**3").m_as("GPa")


def multiplicity_to_spin(multiplicity, n_electrons):
    """
    Convert a standard multiplicity (2S+1) to mopactools' "excess spin"
    convention, per the MopacSystem docstring:
        spin=0 -> singlet (even electrons) or doublet (odd electrons)
        spin=1 -> triplet (even electrons)
    The general pattern (spin=N is N steps of multiplicity-by-2 above the
    minimum state) is an INFERENCE beyond the two cases mopactools
    documents explicitly. Verified consistent with both documented cases;
    not independently confirmed beyond spin=0,1. Treat with appropriate
    caution for higher-spin systems.
    """
    minimum_multiplicity = 1 if (n_electrons % 2 == 0) else 2
    diff = multiplicity - minimum_multiplicity
    if diff < 0 or diff % 2 != 0:
        raise ValueError(
            f"multiplicity {multiplicity} is not reachable for "
            f"{n_electrons} electrons (minimum multiplicity "
            f"{minimum_multiplicity}, must differ by an even number)"
        )
    return diff // 2


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def parse_args():
    p = argparse.ArgumentParser(
        description="MOPAC MDI engine (mopactools API) for LAMMPS fix mdi/qm"
    )
    p.add_argument(
        "-mdi",
        required=True,
        help="MDI initialization string passed directly to MDI_Init",
    )
    # Must match _MDI_CAPABLE_METHODS in mopac_step.py
    p.add_argument(
        "--method",
        default="PM7",
        choices=["PM7", "PM6-D3H4", "PM6-ORG", "PM6", "AM1", "RM1"],
        help="MOPAC semiempirical model (default: PM7)",
    )
    p.add_argument(
        "--charge",
        type=int,
        default=0,
        help="Total charge of the system (default: 0). "
        "Overridden if the driver sends >TOTCHARGE.",
    )
    p.add_argument(
        "--multiplicity",
        type=int,
        default=1,
        help="Standard spin multiplicity, 2S+1 (default: 1, singlet). "
        'Converted internally to mopactools\' "excess spin" convention. '
        "Overridden if the driver sends >ELEC_MULT.",
    )
    p.add_argument(
        "--elements",
        nargs="+",
        metavar="SYM",
        default=None,
        help="Element symbol for each LAMMPS atom type, in order "
        "(e.g. --elements C O H H). Only used as a fallback if the "
        "driver sends >TYPES instead of >ELEMENTS (i.e. if the LAMMPS "
        'fix mdi/qm line omits the "elements" keyword).',
    )
    p.add_argument(
        "--mozyme",
        action="store_true",
        help="Use the linear-scaling MOZYME solver instead of the "
        "conventional solver (closed-shell systems only). Currently "
        "unreliable for periodic liquid MD -- see module docstring.",
    )
    p.add_argument(
        "--mozyme-restart-every",
        type=int,
        default=10,
        metavar="N",
        help="Only relevant with --mozyme. MOPAC's manual documents that "
        "LMO orthonormality degrades gradually when many SCF "
        "calculations are chained together (harmless for one SCF, "
        "cumulative otherwise) -- exactly the situation in an MD run "
        "where the same MozymeState persists across thousands of "
        "steps. Every N calculations, this script discards the "
        "persistent state and builds a fresh MozymeState, forcing "
        "MOPAC to redo its Lewis-structure bonding analysis and "
        "LMO localization from the current geometry rather than "
        "drifting indefinitely. Default of 10 is a placeholder, not "
        "yet confirmed against MOPAC-developer guidance on a safe "
        "interval -- treat as provisional. (default: 10)",
    )
    p.add_argument(
        "--tolerance",
        type=float,
        default=1.0,
        help="Relative SCF convergence tolerance, mopactools default=1.0 "
        "(default: 1.0)",
    )
    p.add_argument(
        "--max-time",
        type=int,
        default=600,
        help="Per-call wall-time limit in seconds (default: 600). "
        "mopactools' own default is 3600; reduced here so a single "
        "stuck MD step does not hang for an hour. Increase for very "
        "large systems if legitimate calculations are being cut off.",
    )
    p.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="DEBUG: every MDI command plus raw energy/stress each call. "
        "INFO: lifecycle events, per-call timing, MOZYME restarts "
        "(default). WARNING: only warnings and errors (quietest).",
    )
    return p.parse_args()


def main():
    args = parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(levelname)s: %(message)s",
        stream=sys.stdout,
    )

    try:
        import mdi
    except ImportError:
        logger.error("mdi not found. conda install -c conda-forge pymdi")
        sys.exit(1)
    try:
        from mopactools.api import MopacSystem, MopacState, MozymeState, from_data
    except ImportError:
        logger.error("mopactools not found. conda install -c conda-forge mopactools")
        sys.exit(1)

    # Optional --elements fallback map (LAMMPS type index -> atomic number),
    # only used if the driver sends >TYPES instead of >ELEMENTS.
    type_to_z = None
    if args.elements is not None:
        type_to_z = {
            i + 1: MopacSystem.periodic_table[sym]
            for i, sym in enumerate(args.elements)
        }

    # ----------------------------------------------------------------
    # MDI initialisation and command registration
    # ----------------------------------------------------------------
    mdi.MDI_Init(args.mdi)
    comm = mdi.MDI_Accept_Communicator()

    mdi.MDI_Register_node("@DEFAULT")
    for _cmd in [
        "<NATOMS",
        ">NATOMS",
        "<NAME",
        ">ELEMENTS",
        ">TYPES",
        ">COORDS",
        ">CELL",
        ">TOTCHARGE",
        ">ELEC_MULT",
        "SCF",
        "<ENERGY",
        "<FORCES",
        "<STRESS",
        "EXIT",
    ]:
        mdi.MDI_Register_command("@DEFAULT", _cmd)

    logger.debug(f"MDI connection established. method={args.method}")

    # ----------------------------------------------------------------
    # State accumulated from the MDI handshake -- no input file at all.
    # ----------------------------------------------------------------
    natoms = None
    atomic_numbers = None
    coords_bohr = None
    cell_flat = None
    is_periodic = False

    charge = args.charge
    raw_multiplicity = args.multiplicity  # may be overridden by >ELEC_MULT

    system = None
    state = None
    properties = None
    have_elements = False
    have_coords = False
    recompute = True
    mozyme_step_count = 0  # calculations since the last MozymeState rebuild

    def build_system():
        """Construct the MopacSystem (once) now that natoms/elements/coords
        (and cell, if periodic) are known. nlattice_move is always set
        equal to nlattice -- see module docstring."""
        nonlocal system, state, mozyme_step_count

        n_electrons = int(np.sum(atomic_numbers)) - charge
        spin = multiplicity_to_spin(raw_multiplicity, n_electrons)

        if args.mozyme and spin != 0:
            logger.warning(
                "--mozyme requested with a non-closed-shell multiplicity; "
                "MozymeState has no spin/uhf field, MOZYME assumes "
                "closed-shell."
            )

        sys_obj = MopacSystem()
        sys_obj.natom = natoms
        sys_obj.natom_move = natoms  # all atoms movable: full gradient
        sys_obj.charge = charge
        sys_obj.spin = spin
        sys_obj.model = args.method
        sys_obj.epsilon = 1.0  # vacuum; explicit solvent, no implicit model
        sys_obj.atom = atomic_numbers.astype(np.int32)
        sys_obj.coord = (coords_bohr.reshape(-1, 3) * ANG_PER_BOHR).ravel()
        if is_periodic:
            sys_obj.nlattice = 3
            sys_obj.nlattice_move = 3  # ALWAYS all-movable: stress workaround
            sys_obj.lattice = (cell_flat.reshape(3, 3) * ANG_PER_BOHR).ravel()
        else:
            sys_obj.nlattice = 0
            sys_obj.nlattice_move = 0
            sys_obj.lattice = np.array([], dtype=np.float64)
        sys_obj.pressure = 0.0  # only relevant to mopac_relax
        sys_obj.tolerance = args.tolerance
        sys_obj.max_time = args.max_time

        if args.mozyme:
            st_obj = MozymeState()
        else:
            st_obj = MopacState()
            st_obj.uhf = spin != 0

        system = sys_obj
        state = st_obj
        mozyme_step_count = 0
        logger.debug(
            f"System built: natoms={natoms}, periodic={is_periodic}, "
            f"charge={charge}, multiplicity={raw_multiplicity} "
            f"(spin={spin}), mozyme={args.mozyme}"
        )

    def maybe_restart_mozyme():
        """Every --mozyme-restart-every calculations, discard the
        persistent MozymeState and build a fresh one, forcing MOPAC to
        redo Lewis-structure bonding analysis and LMO localization from
        the current geometry rather than letting orthonormality drift
        indefinitely across thousands of MD steps. See the
        --mozyme-restart-every help text and MOPAC's MOZYME manual page."""
        nonlocal state
        if (
            args.mozyme
            and mozyme_step_count > 0
            and mozyme_step_count % args.mozyme_restart_every == 0
        ):
            logger.debug(
                f"MOZYME restart (count={mozyme_step_count}): "
                f"rebuilding LMOs from current geometry"
            )
            state = MozymeState()

    def update_geometry():
        """Push the latest coordinates/cell into the existing system
        object. Called every step once the system has been built."""
        system.coord = (coords_bohr.reshape(-1, 3) * ANG_PER_BOHR).ravel()
        if is_periodic:
            system.lattice = (cell_flat.reshape(3, 3) * ANG_PER_BOHR).ravel()

    def run_calculation():
        """Run mopac_scf/mozyme_scf (dispatched by from_data based on the
        state type) and check for reported errors."""
        nonlocal properties
        mpack_before = getattr(state, "mpack", None)
        t0 = time.perf_counter()
        properties = from_data(system, state, relax=False, vibe=False)
        elapsed = time.perf_counter() - t0
        mpack_after = getattr(state, "mpack", None)
        logger.debug(
            f"from_data() took {elapsed:.3f} s "
            f"(state.mpack: {mpack_before} -> {mpack_after})"
        )
        if properties.error_msg:
            raise RuntimeError(
                "MOPAC reported error(s): " + "; ".join(properties.error_msg)
            )
        logger.debug(
            f"heat = {properties.heat:.8f} kcal/mol "
            f"({properties.heat * HARTREE_PER_KCALMOL:.8f} Ha)"
        )
        if is_periodic and properties.stress is not None:
            logger.debug(f"stress (raw, GPa, Voigt): {properties.stress}")

    # ----------------------------------------------------------------
    # MDI event loop
    # ----------------------------------------------------------------
    logger.debug("Entering MDI event loop ...")

    while True:
        command = mdi.MDI_Recv_Command(comm)
        logger.debug(f"command: {command!r}")

        # ---- Metadata -------------------------------------------------
        if command == "<NATOMS":
            mdi.MDI_Send(natoms, 1, mdi.MDI_INT, comm)

        elif command == ">NATOMS":
            raw = mdi.MDI_Recv(1, mdi.MDI_INT, comm)
            natoms = int(np.asarray(raw).flat[0])
            atomic_numbers = np.zeros(natoms, dtype=int)
            coords_bohr = np.zeros(3 * natoms)
            logger.debug(f">NATOMS: {natoms}")

        elif command == "<NAME":
            mdi.MDI_Send("MOPAC", mdi.MDI_NAME_LENGTH, mdi.MDI_CHAR, comm)

        # ---- Structural data from the driver ---------------------------
        elif command == ">ELEMENTS":
            # Preferred path: driver sends atomic numbers directly.
            raw = mdi.MDI_Recv(natoms, mdi.MDI_INT, comm)
            atomic_numbers[:] = np.asarray(raw)
            have_elements = True
            recompute = True

        elif command == ">TYPES":
            # Fallback path: driver sends LAMMPS atom types; need --elements
            # to map type -> atomic number ourselves.
            if type_to_z is None:
                raise RuntimeError(
                    ">TYPES received but no --elements mapping was given. "
                    "Either add 'elements <syms>' to the LAMMPS fix mdi/qm "
                    "line (sends >ELEMENTS instead), or pass --elements here."
                )
            raw = mdi.MDI_Recv(natoms, mdi.MDI_INT, comm)
            types = np.asarray(raw)
            atomic_numbers[:] = [type_to_z[t] for t in types]
            have_elements = True
            recompute = True

        elif command == ">COORDS":
            raw = mdi.MDI_Recv(3 * natoms, mdi.MDI_DOUBLE, comm)
            coords_bohr[:] = np.asarray(raw)
            have_coords = True
            recompute = True

        elif command == ">CELL":
            raw = mdi.MDI_Recv(9, mdi.MDI_DOUBLE, comm)
            cell_flat = np.asarray(raw)
            is_periodic = True
            recompute = True

        # ---- Optional driver-supplied charge/multiplicity --------------
        elif command == ">TOTCHARGE":
            raw = mdi.MDI_Recv(1, mdi.MDI_DOUBLE, comm)
            charge = int(round(float(np.asarray(raw).flat[0])))
            system = None  # force rebuild with new charge
            recompute = True

        elif command == ">ELEC_MULT":
            raw = mdi.MDI_Recv(1, mdi.MDI_INT, comm)
            raw_multiplicity = int(np.asarray(raw).flat[0])
            system = None  # force rebuild with new multiplicity
            recompute = True

        # ---- Calculation trigger / lazy evaluation ---------------------
        elif command in ("SCF", "<ENERGY", "<FORCES", "<STRESS"):
            if recompute or system is None:
                if not (have_elements and have_coords):
                    raise RuntimeError(
                        f"{command} requested before elements/coords were "
                        f"received via MDI -- check the driver sends "
                        f">ELEMENTS (or >TYPES) and >COORDS before "
                        f"requesting properties."
                    )
                if system is None:
                    build_system()
                else:
                    maybe_restart_mozyme()
                    update_geometry()
                run_calculation()
                mozyme_step_count += 1
                recompute = False

            # Property responses (no-op for plain "SCF")
            if command == "<ENERGY":
                mdi.MDI_Send(
                    properties.heat * HARTREE_PER_KCALMOL, 1, mdi.MDI_DOUBLE, comm
                )

            elif command == "<FORCES":
                # coord_deriv = dE/dx [kcal/(mol*Ang)]; force = -dE/dx
                grad_kcal_ang = properties.coord_deriv.reshape(-1, 3)
                grad_ha_bohr = (grad_kcal_ang * HARTREE_PER_KCALMOL) * BOHR_PER_ANG
                forces = -grad_ha_bohr.ravel()
                mdi.MDI_Send(forces, 3 * natoms, mdi.MDI_DOUBLE, comm)

            elif command == "<STRESS":
                if not is_periodic:
                    raise RuntimeError("<STRESS requested for a non-periodic system")
                voigt = properties.stress  # GPa, Voigt (xx,yy,zz,yz,xz,xy), tensile+
                # Voigt -> full 3x3 tensor (symmetric placement)
                full = np.array(
                    [
                        [voigt[0], voigt[5], voigt[4]],
                        [voigt[5], voigt[1], voigt[3]],
                        [voigt[4], voigt[3], voigt[2]],
                    ]
                )
                # Negate (tensile+ -> compressive+) and convert GPa -> Ha/Bohr^3
                stress_ha_bohr3 = -full / GPA_PER_HARTREE_BOHR3
                mdi.MDI_Send(stress_ha_bohr3.ravel(), 9, mdi.MDI_DOUBLE, comm)

        # ---- Shutdown ---------------------------------------------------
        elif command == "EXIT":
            logger.debug("EXIT -- shutting down.")
            break

        else:
            logger.warning(f"unrecognised command {command!r}")

    logger.debug("Done.")


if __name__ == "__main__":
    main()
