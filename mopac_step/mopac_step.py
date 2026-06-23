# mopac_step/mopac_step.py
# -*- coding: utf-8 -*-

"""Main module."""

import configparser
import importlib.resources
import os
import shutil
from pathlib import Path

import mopac_step


class MOPACStep(object):
    my_description = {
        "description": "Setup and run MOPAC",
        "group": "Simulations",
        "name": "MolSSI MOPAC",
    }

    def __init__(self, flowchart=None, gui=None):
        """Initialize this helper class, which is used by
        the application via stevedore to get information about
        and create node objects for the flowchart
        """
        pass

    def description(self):
        """Return a description of what this extension does"""
        return MOPACStep.my_description

    def create_node(self, flowchart=None, **kwargs):
        """Return the new node object"""
        return mopac_step.MOPAC(flowchart=flowchart, **kwargs)

    def create_tk_node(self, canvas=None, **kwargs):
        """Return the graphical Tk node object"""
        return mopac_step.TkMOPAC(canvas=canvas, **kwargs)

    # Patch to mopac_step/mopac_step.py -- add to the MOPACStep class,
    # alongside description()/create_node()/create_tk_node().
    #
    # Revision 2026-06-22: now surfaces "sparkle_elements" in the returned
    # dict (added to the raw metadata for PM7/PM7-TS/PM6ants on 2026-06-22, but
    # the first draft of this classmethod predated that field and never
    # passed it through -- caught while writing tests, fixed here).

    # mopactools.api.MopacSystem.model_dict's scope -- see mopac_mdi.py's
    # --method choices. This is the authoritative source for what's
    # actually reachable via MDI; update here if mopactools changes.

    _MDI_CAPABLE_METHODS = {"PM7", "PM6-D3H4", "PM6-ORG", "PM6", "AM1", "RM1"}

    # Methods actually run periodic via MDI and confirmed working, per
    # NOTES_qm_mdi_engines_validation.rst. Cross-checked against the real
    # metadata["computational models"] entries -- PM7, PM6, and PM6-ORG are
    # the only three with both periodic=True there AND an actual validated
    # periodic MDI run this week. PM6-D3H4 is MDI-capable but deliberately
    # excluded: its own metadata entry says periodic=False, and MOPAC's
    # documentation confirms D3H4 does not work under periodic boundary
    # conditions at all.

    _MDI_PERIODIC_VALIDATED = {"PM7", "PM6-ORG", "PM6"}

    @classmethod
    def get_model_chemistry_options(cls, periodic_only=False, mdi_only=False):
        """Return the model chemistries MOPAC can provide.

        NOTE: only covers methods present in metadata["computational
        models"]. As of 2026-06-22 this includes PM7, PM7-TS, PM6,
        PM6-ORG, PM6-D3, PM6-DH+, PM6-DH2, PM6-DH2X, PM6-D3H4, PM6-D3H4X,
        AM1, RM1, PM3, MNDO, MNDOD.

        Parameters
        ----------
        periodic_only : bool
            Only return options confirmed to work for a periodic system
            via MDI -- conservative by design, a method is only included
            if it has actually been run periodic and validated, not
            because some other flag suggests it should work.
        mdi_only : bool
            Only return options actually launchable via mopac_mdi.py, as
            opposed to only available through this step's traditional
            batch/file-based path.

        Returns
        -------
        dict
            Keyed by bare method name (e.g. "PM6-ORG"). Each value has::

                model_chemistry  : str   -- "MOPAC:SQM@<name>"
                type             : str   -- always "SQM" currently
                description      : str
                periodic_native  : bool  -- this method's own metadata flag
                periodic_mdi     : bool  -- actually validated periodic via MDI
                elements         : str   -- genuine NDDO Hamiltonian coverage
                sparkle_elements : str or None -- lanthanides reachable only
                                   via the Sparkle point-charge model
                                   (currently documented for PM7/PM7-TS/PM6
                                   only; None elsewhere, which may mean "not
                                   applicable" or "not yet checked" -- see
                                   NOTES_mopac_model_chemistry_metadata.rst)
                mdi_capable      : bool
                mdi_script       : str or None
                mdi_method_arg   : str or None
        """
        options = {}
        for theory_class, class_data in mopac_step.metadata[
            "computational models"
        ].items():
            for family, family_data in class_data["models"].items():
                for name, param in family_data["parameterizations"].items():
                    mdi_capable = name in cls._MDI_CAPABLE_METHODS
                    periodic_mdi = name in cls._MDI_PERIODIC_VALIDATED

                    if periodic_only and not periodic_mdi:
                        continue
                    if mdi_only and not mdi_capable:
                        continue

                    options[name] = {
                        "model_chemistry": f"MOPAC:SQM@{name}",
                        "type": "SQM",
                        "description": param.get("description", ""),
                        "periodic_native": param.get("periodic", False),
                        "periodic_mdi": periodic_mdi,
                        "elements": param.get("elements", ""),
                        "sparkle_elements": param.get("sparkle_elements"),
                        "mdi_capable": mdi_capable,
                        "mdi_method_arg": name if mdi_capable else None,
                    }
        return options

    # Patch to mopac_step/mopac_step.py -- add to the MOPACStep class,
    # alongside get_model_chemistry_options().
    #
    # 2026-06-23: executor configuration for the MDI engine (Option C --
    # the engine script is shipped inside this package, at
    # data/mopac_mdi.py, so it is refreshed by `pip install -U mopac-step`
    # and never depends on the user re-running the step installer to
    # refresh the seamm-mopac environment).

    @classmethod
    def get_executor_config(cls, executor, seamm_options):
        """Return how to launch MOPAC (and its MDI engine) on this machine.

        Reads the per-plug-in ``mopac.ini`` for the *current* executor type
        exactly as ``MOPAC.run()`` does, so the MDI engine runs in the same
        conda/local/modules/docker environment as ordinary MOPAC jobs. Adds
        one key, ``mdi_script`` -- the absolute path to the bundled
        ``data/mopac_mdi.py`` engine.

        ``mopac_mdi.py`` imports only packages present in ``seamm-mopac``
        (``mopactools``, ``pymdi``/``mdi``, ``numpy``, ``seamm_util``) and
        nothing from ``mopac_step`` or ``seamm``, so it runs correctly under
        that environment's Python even though the file physically lives in
        the ``seamm`` environment's site-packages.

        Parameters
        ----------
        executor : seamm.ExecutorBase
            The flowchart executor, typically ``self.flowchart.executor`` in
            the calling (driver) step. ``executor.name`` selects the ini
            section.
        seamm_options : dict
            The global SEAMM options, typically ``self.global_options`` in
            the calling step. ``seamm_options["root"]`` locates the ini.

        Returns
        -------
        dict
            The ini section for the current executor (``installation``,
            ``code``, ``conda``, ``conda-environment``, ...), plus::

                version    : str  -- this plug-in's version (container tag)
                mdi_script : str  -- absolute path to data/mopac_mdi.py
        """
        executor_type = executor.name
        ini_dir = Path(seamm_options["root"]).expanduser()
        ini_path = ini_dir / "mopac.ini"
        resources = importlib.resources.files("mopac_step") / "data"

        # Bootstrap a default mopac.ini if the user has none yet, mirroring
        # the [local] conda/conda-environment defaults written by
        # MOPAC.run(). Written with configparser primitives to avoid pulling
        # in seamm_util.Configuration here. In practice mopac.ini almost
        # always already exists by the time an MDI run is launched, since
        # seamm-mopac must be installed for the engine to import mopactools.
        if not ini_path.exists():
            boot = configparser.ConfigParser()
            boot.read_string((resources / "mopac.ini").read_text())
            if "local" not in boot:
                boot.add_section("local")
            boot["local"]["conda"] = os.environ["CONDA_EXE"]
            boot["local"]["conda-environment"] = "seamm-mopac"
            with ini_path.open("w") as fd:
                boot.write(fd)

        full_config = configparser.ConfigParser()
        full_config.read(ini_path)

        # Last-ditch: fall back to an executable on $PATH.
        if executor_type not in full_config:
            path = shutil.which("mopac")
            if path is None:
                raise RuntimeError(
                    f"No section for '{executor_type}' in the MOPAC ini file "
                    f"({ini_path}), nor in the defaults, nor on $PATH."
                )
            full_config.add_section(executor_type)
            full_config.set(executor_type, "installation", "local")
            full_config.set(executor_type, "code", str(path))
            with ini_path.open("w") as fd:
                full_config.write(fd)

        config = dict(full_config.items(executor_type))
        config["version"] = mopac_step.__version__
        config["mdi_script"] = str(resources / "mopac_mdi.py")
        return config

    @classmethod
    def get_mdi_engine_command(
        cls,
        executor,
        seamm_options,
        *,
        method,
        port,
        hostname="localhost",
        charge=0,
        multiplicity=1,
        engine_name="MOPAC",
        extra_args=None,
    ):
        """Build the argv that launches the MOPAC MDI *engine* over TCP.

        The MDI transport coordination (TCP, ``port``, ``hostname``) is
        decided by the *driver* (e.g. lammps_step), which owns the rendezvous
        and must give the same values to both sides, and is passed in here.
        Everything MOPAC-specific -- the conda environment, the bundled
        ``mopac_mdi.py`` path, the engine's MDI name, and the method /
        charge / multiplicity flags -- is supplied by this step, so the
        driver hardwires no MOPAC knowledge.

        Parameters
        ----------
        executor, seamm_options
            Passed straight to ``get_executor_config`` to locate the conda
            environment and the bundled engine script.
        method : str
            Semiempirical method, e.g. "PM6-ORG". Must be one of
            ``cls._MDI_CAPABLE_METHODS`` (== the engine's --method choices).
        port : int
            TCP port the engine binds; chosen by the driver.
        hostname : str
            Host the engine binds / the driver connects to (default
            "localhost").
        charge, multiplicity : int
            Default total charge and 2S+1 multiplicity. Overridden at run
            time if the driver sends >TOTCHARGE / >ELEC_MULT (LAMMPS's
            fix mdi/qm currently does not).
        engine_name : str
            The MDI ``-name`` for the engine and what it returns for <NAME;
            must match the driver's expectation (default "MOPAC").
        extra_args : list of str, optional
            Extra engine flags appended verbatim, e.g.
            ``["--mozyme", "--tolerance", "0.5"]``.

        Returns
        -------
        list of str
            A ready-to-run argv. Render into the launch script with
            ``shlex.join(argv)``.
        """
        if method not in cls._MDI_CAPABLE_METHODS:
            raise ValueError(
                f"'{method}' is not an MDI-capable MOPAC method; expected "
                f"one of {sorted(cls._MDI_CAPABLE_METHODS)}."
            )

        config = cls.get_executor_config(executor, seamm_options)

        installation = config.get("installation", "conda")
        if installation != "conda":
            raise NotImplementedError(
                "The MOPAC MDI engine is currently wired up only for a conda "
                f"installation; mopac.ini selects '{installation}'. "
                "TODO (Phase B+): local / modules / docker launches."
            )

        mdi_init = (
            f"-role ENGINE -name {engine_name} -method TCP "
            f"-port {port} -hostname {hostname}"
        )

        argv = [
            config["conda"],
            "run",
            "--live-stream",
            "-n",
            config["conda-environment"],
            "python",
            config["mdi_script"],
            "-mdi",
            mdi_init,
            "--method",
            method,
            "--charge",
            str(charge),
            "--multiplicity",
            str(multiplicity),
        ]
        if extra_args:
            argv.extend(extra_args)
        return argv
