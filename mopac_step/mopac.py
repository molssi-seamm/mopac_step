# -*- coding: utf-8 -*-

"""Setup and run MOPAC"""

import calendar
import configparser
from datetime import datetime
import importlib
import logging
import os
import os.path
from pathlib import Path
import pprint
import re
import shutil
import string


import molsystem
import seamm
import seamm_exec
from seamm_util import Configuration
import seamm_util.printing as printing
from seamm_util.printing import FormattedText as __
import mopac_step

logger = logging.getLogger(__name__)
job = printing.getPrinter()
printer = printing.getPrinter("mopac")

# Add MOPAC's properties to the standard properties
resources = importlib.resources.files("mopac_step") / "data"
csv_file = resources / "properties.csv"
molsystem.add_properties_from_file(csv_file)


def estimated_seconds(keyword_lines, n_atoms):
    """A rough estimate of a MOPAC run's time, for the inline rule.

    Tens of milliseconds for a small molecule; the SCF scales roughly as the
    cube of the size, and a geometry optimization or frequencies take many SCFs.
    """
    n = max(1, int(n_atoms))
    total = 0.0
    for line in keyword_lines:
        words = line.upper().split()
        scf = 0.02 + 2.0e-6 * n**3
        if (
            "FORCE" in words
            or "THERMO" in words
            or any(w.startswith("THERMO") for w in words)
        ):
            scf *= 6 * n
        elif "1SCF" not in words:
            scf *= 30  # an optimization
        total += scf
    return total


#: What MOPAC's cost model is made of (seamm_exec.timing_model.Spec as plain
#: data): basis functions and atoms as size variables, the Hamiltonian and the
#: regime (scf or mozyme) as the method class, the task, SCFs as the unit; one
#: core, so no parallel exponent.
TIMING_SPEC = {
    "size": ["n_basis", "n_atoms"],
    "klass": ["hamiltonian", "regime"],
    "task": "task",
    # An optimization's time is its geometry cycles (an SCF and a gradient
    # each), not its SCF count, which MOPAC reports as 1 or 2 however long it
    # runs; a single point has none, which counts as one.
    "units": "geometry_cycles",
    "multiplier": None,
    "default_alpha": 0.0,
    # MOZYME (localized orbitals) scales roughly linearly and the traditional
    # SCF roughly as N^3: each regime has its own size exponent.
    "slope_by": "regime",
    # MOZYME pays a large setup (localizing the orbitals) once per job, then
    # runs fast cycles: each regime has its own fixed cost, in cycles.
    "setup_by": "regime",
}

#: The Energy sub-step's MOZYME follow-up that runs a traditional SCF
_EXACT_FOLLOW_UP = (
    "recalculate the energy at the end using exact, non-localized orbitals"
)


#: The molecules the timing benchmark runs, by size (atoms): three orders of
#: magnitude, each built from SMILES; the alkanes reach MOZYME's territory
_BENCHMARK_MOLECULES = (
    ("water", "O", 3),
    ("ethanol", "CCO", 9),
    ("toluene", "Cc1ccccc1", 15),
    ("caffeine", "Cn1cnc2c1c(=O)n(C)c(=O)n2C", 24),
    ("icosane", "C" * 20, 62),
    ("hectane", "C" * 100, 302),
    ("alkane-300", "C" * 300, 902),
    ("alkane-1000", "C" * 1000, 3002),
)

#: The step's timing benchmark (seamm_exec.timing_benchmark). MOPAC does not
#: take the Model Chemistry: the Hamiltonian is a parameter of its sub-steps,
#: set from the chemistry key. It runs on one core, so no core sweep. From 300
#: atoms both regimes run: MOZYME (the default there) and the traditional SCF
#: forced, to 902 atoms (its N^3 makes 3002 too long).
TIMING_BENCHMARK = {
    "program": "mopac",
    "step": "MOPAC",
    "section": "mopac-step",
    "parallel": False,
    "systems": [
        {
            "name": name,
            "size": n_atoms,
            "steps": [{"FromSMILESStep": {"smiles string": smiles}}],
        }
        for name, smiles, n_atoms in _BENCHMARK_MOLECULES
    ],
    "chemistries": {
        "PM7": {"quick": 902, "full": 3002},
        "PM6-ORG": {"quick": 302, "full": 902},
    },
    "parameter": "hamiltonian",
    "tasks": {
        "Energy": {"quick": 902, "full": 3002},
        "Optimization": {"quick": 62, "full": 302},
    },
    "variants": {
        # From 300 atoms, where MOZYME is used: the default follow-up (fresh
        # localized orbitals), the traditional SCF forced, and the follow-up
        # that runs a traditional SCF after MOZYME (to 902 atoms: its N^3)
        "Energy": [
            {},
            {"MOZYME": "never", "_min_size": 300, "_max_size": 902},
            {"MOZYME follow-up": _EXACT_FOLLOW_UP, "_min_size": 300, "_max_size": 902},
        ],
        "Optimization": [
            {},
            {"MOZYME follow-up": _EXACT_FOLLOW_UP, "_min_size": 300},
        ],
    },
}


def _record_kwargs():
    """``spec=`` for seamm-exec releases that take it (2026.10.6.1 on)."""
    return {"spec": TIMING_SPEC} if hasattr(seamm_exec, "TimingSpec") else {}


#: MOPAC Hamiltonians, for the timing records
_HAMILTONIANS = (
    "PM7",
    "PM6-ORG",
    "PM6-D3H4X",
    "PM6-D3H4",
    "PM6-D3",
    "PM6",
    "RM1",
    "AM1",
    "MNDOD",
    "MNDO",
    "PM3",
)


def task_kind(keyword_lines):
    """What kind of calculation a MOPAC input asks for, for the timing records:
    the most expensive over its calculations -- ``force`` (FORCE/THERMO, a
    Hessian), ``opt`` (anything without 1SCF), ``gradient`` (1SCF GRADIENTS) or
    ``energy``."""
    kinds = []
    for line in keyword_lines:
        words = set(line.upper().split())
        if (
            "FORCE" in words
            or "FORCETS" in words
            or any(w.startswith("THERMO") for w in words)
        ):
            kinds.append("force")
        elif "1SCF" not in words:
            kinds.append("opt")
        elif "GRADIENTS" in words or "GRADIENT" in words:
            kinds.append("gradient")
        else:
            kinds.append("energy")
    for kind in ("force", "opt", "gradient", "energy"):
        if kind in kinds:
            return kind
    return "energy"


def timing_descriptors(keyword_lines, output_text, configuration=None):
    """The descriptors of a MOPAC run for its timing record (seamm_exec's
    campaign of 2026-10-05): the Hamiltonian, the kind of task, the regime --
    ``mozyme`` (localized orbitals, roughly linear in the size) or ``scf``
    (the traditional SCF, N^2-N^3 in the basis functions) -- read from the
    output, since MOZYME may not be used even when asked for; the number of
    basis functions (4 per heavy atom, 1 per hydrogen); and from the output
    the SCFs converged, the geometry cycles and MOPAC's own job time.
    """
    # The same columns in every record (a change of columns sets the timing
    # file aside): which job of the run, and what follow-up it is, if any
    d = {"job": 1, "follow_up": ""}
    text = " ".join(keyword_lines).upper()
    words = text.split()
    d["hamiltonian"] = next((h for h in _HAMILTONIANS if h in words), "")
    d["task"] = task_kind(keyword_lines)
    d["n_calculations"] = len(keyword_lines)
    d["keywords"] = " && ".join(keyword_lines)
    d["mozyme_requested"] = "MOZYME" in words
    if configuration is not None:
        d.update(seamm_exec.structure_descriptors(configuration))
        if "n_atoms" in d:
            d["n_basis"] = 4 * d["n_heavy"] + (d["n_atoms"] - d["n_heavy"])
    if output_text:
        d["regime"] = (
            "mozyme" if re.search(r"^ \*\s+MOZYME\b", output_text, re.M) else "scf"
        )
        d["scf_runs"] = len(re.findall(r"SCF FIELD WAS ACHIEVED", output_text))
        d["geometry_cycles"] = len(re.findall(r"^ CYCLE:\s+\d+", output_text, re.M))
        # MOPAC's clock is cumulative over the jobs of an input, and its
        # "TOTAL JOB TIME" adds those cumulative values, so it overstates a
        # run of several jobs: the last WALL-CLOCK TIME is the run's time.
        clocks = _WALL_CLOCK.findall(output_text)
        if clocks:
            d["code_seconds"] = float(clocks[-1])
        else:
            m = re.search(r"TOTAL JOB TIME:\s+([\d.]+)\s+SECONDS", output_text)
            d["code_seconds"] = float(m.group(1)) if m else None
        d["terminated_normally"] = "== MOPAC DONE ==" in output_text
    return d


_WALL_CLOCK = re.compile(r"WALL-CLOCK TIME\s+=\s+([\d.]+)\s+SECONDS")


def job_descriptors(keyword_lines, output_text, configuration=None):
    """The descriptors of each job of a MOPAC run, one dict per job, or None
    when the output cannot be split into the input's jobs.

    An input may hold several jobs: a MOZYME calculation and its follow-up (a
    single point with fresh localized orbitals, or with a traditional SCF). Each
    is its own calculation for the cost model -- its regime, cycles and time --
    so a traditional-SCF follow-up is not counted as MOZYME. The output is split
    at the cumulative WALL-CLOCK TIME MOPAC prints after each job; each job's
    time is the difference. A follow-up is marked with ``follow_up``: ``exact``
    (traditional SCF) or ``new`` (fresh localized orbitals).
    """
    if not output_text or len(keyword_lines) < 2:
        return None
    ends = [m.end() for m in _WALL_CLOCK.finditer(output_text)]
    clocks = [float(c) for c in _WALL_CLOCK.findall(output_text)]
    if len(ends) != len(keyword_lines):
        return None
    jobs = []
    start, previous = 0, 0.0
    for i, (line, end, clock) in enumerate(zip(keyword_lines, ends, clocks)):
        segment = output_text[start:end]
        d = timing_descriptors([line], segment, configuration)
        d["code_seconds"] = max(0.0, clock - previous)
        d["job"] = i + 1
        d["n_calculations"] = len(keyword_lines)
        d["terminated_normally"] = "== MOPAC DONE ==" in output_text
        words = set(line.upper().split())
        if i > 0 and "OLDGEO" in words and "1SCF" in words:
            d["follow_up"] = "new" if "MOZYME" in words else "exact"
        jobs.append(d)
        start, previous = end, clock
    return jobs


def reuse_previous_run(directory, text):
    """Whether a finished MOPAC run in ``directory`` can be reused for ``text``.

    Only when it succeeded (``success.dat``) with the same input (``mopac.dat``);
    a marker left by a run of other input is removed, so the calculation runs.
    """
    directory = Path(directory)
    success = directory / "success.dat"
    if not success.exists():
        return False
    previous = directory / "mopac.dat"
    if previous.exists() and previous.read_text() == text:
        return True
    success.unlink()
    return False


class MOPAC(mopac_step.MOPACBase):
    def __init__(
        self,
        flowchart=None,
        namespace="org.molssi.seamm.mopac",
        extension=None,
        title="MOPAC",
        logger=logger,
    ):
        """Initialize the node"""

        logger.debug("Creating MOPAC {}".format(self))

        # Create the subflowchart and proceed
        if title == "MOPAC":
            self.subflowchart = seamm.Flowchart(
                name="MOPAC",
                parent=self,
                namespace=namespace,
                directory=flowchart.root_directory,
            )
        self._data = {}
        self._lattice_opt = True
        self._lattice_shear = True
        self._lattice_couple = "none"
        self._input_only = False

        super().__init__(
            flowchart=flowchart, title=title, extension=extension, logger=logger
        )

    @property
    def input_only(self):
        """Whether to write the input only, not run MOPAC."""
        return self._input_only

    @input_only.setter
    def input_only(self, value):
        self._input_only = value

    def description_text(self, P=None):
        """Return a short description of this step.

        Return a nicely formatted string describing what this step will
        do.

        Keyword arguments:
            P: a dictionary of parameter values, which may be variables
                or final values. If None, then the parameters values will
                be used as is.
        """
        # Work through children. Get the first real node
        node = self.subflowchart.get_node("1").next()

        text = self.header + "\n\n"
        while node is not None:
            text += __(node.description_text(), indent=4 * " ").__str__()
            text += "\n"
            node = node.next()

        return text

    def run(self, printer=printer):
        """Run MOPAC"""
        # Create the directory
        directory = Path(self.directory)
        directory.mkdir(parents=True, exist_ok=True)

        next_node = super().run(printer)

        system, configuration = self.get_system_configuration(None)
        n_atoms = configuration.n_atoms
        if n_atoms == 0:
            self.logger.error("MOPAC run(): there is no structure!")
            raise RuntimeError("MOPAC run(): there is no structure!")

        # Print our header to the main output
        printer.normal(self.header)
        printer.normal("")

        # Access the options
        options = self.options
        seamm_options = self.global_options

        extra_keywords = ["AUX(MOS=10,XP,XS,PRECISION=3)"]

        # Always add the charge since that will cause MOZYME, if used, to check.
        extra_keywords.append(f"CHARGE={configuration.charge}")
        # And the spin multiplicity
        multiplicity = configuration.spin_multiplicity
        if multiplicity <= 10:
            extra_keywords.append(
                (
                    "SINGLET",
                    "DOUBLET",
                    "TRIPLET",
                    "QUARTET",
                    "QUINTET",
                    "SEXTET",
                    "SEPTET",
                    "OCTET",
                    "NONET",
                )[multiplicity - 1]
            )
        else:
            extra_keywords.append(f"MS={(multiplicity - 1) / 2}")

        n_active_electrons = configuration.n_active_electrons
        n_active_orbitals = configuration.n_active_orbitals

        if n_active_orbitals > 0:
            extra_keywords.append(f"OPEN({n_active_electrons},{n_active_orbitals})")
            state = configuration.state
            if state != "1":
                extra_keywords.append(f"ROOT={state}")
        else:
            if multiplicity > 1:
                extra_keywords.append("UHF")

        # All Lanthanides (except La and Lu) must use the SPARKLES keyword.
        # La and Lu use the SPARKLES keyword optionally, depending
        # if you're looking for good structure (do use SPARKLES) or
        # energy (do not use SPARKLES)
        La = [
            "Ce",
            "Pr",
            "Nd",
            "Pm",
            "Sm",
            "Eu",
            "Gd",
            "Tb",
            "Dy",
            "Ho",
            "Er",
            "Tm",
            "Yb",
        ]

        La_list = set(La) & set(configuration.atoms.symbols)

        if len(La_list) > 0:
            extra_keywords.append("SPARKLES")

        # if mopac_num_threads > 1:
        #     extra_keywords.append("THREADS={}".format(mopac_num_threads))

        # Work through the subflowchart to find out what to do.
        self.subflowchart.root_directory = self.flowchart.root_directory

        # Get the first real node
        node = self.subflowchart.get_node("1").next()

        text = ""
        n_calculations = []
        all_keywords = []
        while node:
            node.parent = self
            inputs = node.get_input()
            n_calculations.append(len(inputs))
            for keywords, structure, comment in inputs:
                lines = []
                if "OLDGEO" not in keywords:
                    structure_lines, symlines = self.mopac_structure()
                    if symlines != "" and "SYMMETRY" not in extra_keywords:
                        extra_keywords.append("SYMMETRY")
                else:
                    symlines = ""
                all_keywords.append(" ".join(keywords + extra_keywords))
                lines.append(" ".join(keywords + extra_keywords))
                lines.append(system.name)
                if comment is None:
                    lines.append(configuration.name)
                else:
                    lines.append(comment)

                text += "\n".join(lines)
                text += "\n"
                if structure is None:
                    if "OLDGEO" not in keywords:
                        text += structure_lines
                        text += "\n"
                        if symlines != "":
                            text += symlines
                            text += "\n"
                else:
                    text += structure_lines
                    text += "\n"
            node = node.next()

        # Check for successful run, don't rerun -- but only of the same input:
        # a marker left by a run with other input would give the old results.
        output = ""  # Text output to print
        if reuse_previous_run(directory, text):
            pass
        else:
            # Input files
            files = {"mopac.dat": text}
            self.logger.debug("mopac.dat:\n" + files["mopac.dat"])
            for filename in files:
                path = directory / filename
                path.write_text(files[filename])

            if not self.input_only:
                # Get the computational environment and set limits
                ce = seamm_exec.computational_environment()

                n_cores = ce["NTASKS"]
                if seamm_options["ncores"] != "available":
                    n_cores = min(n_cores, int(seamm_options["ncores"]))
                # Currently, on the Mac, it is not clear that any parallelism helps
                # much.

                n_hydrogens = configuration.atoms.get_n_atoms("atno", "==", 1)
                n_basis = (n_atoms - n_hydrogens) * 4 + n_hydrogens
                if options["ncores"] == "default":
                    # Since it is the matrix diagonalization, work out rough
                    # size of matrix

                    # Wild guess!
                    # tmp = max(1, int(pow(n_basis / 1000, 3)))
                    # if tmp < n_cores:
                    #     n_cores = tmp

                    # It appears that MOPAC gets little benefit from parallel,
                    # so run serial
                    tmp = 1
                else:
                    tmp = int(options["ncores"])
                if tmp < n_cores:
                    n_cores = tmp
                if n_cores < 1:
                    n_cores = 1
                ce["NTASKS"] = n_cores

                output = (
                    f"MOPAC will use {n_cores} threads for {n_atoms} atoms with "
                    f"{n_basis} basis functions."
                )
                output = __(output, indent=8 * " ")

                env = {
                    "OMP_NUM_THREADS": str(n_cores),
                }

                executor = self.flowchart.executor

                # Read configuration file for MOPAC if it exists
                executor_type = executor.name
                full_config = configparser.ConfigParser()
                ini_dir = Path(seamm_options["root"]).expanduser()
                path = ini_dir / "mopac.ini"
                # If the config file doesn't exists, get the default
                if not path.exists():
                    resources = importlib.resources.files("mopac_step") / "data"
                    ini_text = (resources / "mopac.ini").read_text()
                    txt_config = Configuration(path)
                    txt_config.from_string(ini_text)

                    # Work out the conda info needed
                    txt_config.set_value("local", "conda", os.environ["CONDA_EXE"])
                    txt_config.set_value("local", "conda-environment", "seamm-mopac")
                    txt_config.save()

                full_config.read(ini_dir / "mopac.ini")

                # Getting desperate! Look for an executable in the path
                if executor_type not in full_config:
                    path = shutil.which("mopac")
                    if path is None:
                        raise RuntimeError(
                            f"No section for '{executor_type}' in MOPAC ini file "
                            f"({ini_dir / 'mopac.ini'}), nor in the defaults, nor "
                            "in the path!"
                        )
                    else:
                        txt_config = Configuration(path)
                        txt_config.add_section(executor_type)
                        txt_config.set_value(executor_type, "installation", "local")
                        txt_config.set_value(executor_type, "code", str(path))
                        txt_config.save()
                        full_config.read(ini_dir / "mopac.ini")

                config = dict(full_config.items(executor_type))

                return_files = [
                    "mopac.arc",
                    "mopac.out",
                    "mopac.aux",
                    "stdout.txt",
                    "stderr.txt",
                ]

                # In place (in_situ=True), so MOPAC's output can be watched
                # as it runs (mopac_step#155).
                task = seamm_exec.Task(
                    key="mopac",
                    program="mopac",
                    cmd=["{code}", "mopac.dat", ">", "stdout.txt", "2>", "stderr.txt"],
                    config=config,
                    directory=self.directory,
                    files=files,
                    return_files=return_files,
                    in_situ=True,
                    shell=True,
                    env=env,
                    resources=seamm_exec.Resources(ntasks=1, cpus_per_task=n_cores),
                    estimated_seconds=estimated_seconds(all_keywords, n_atoms),
                )
                result = seamm_exec.run_task(task, node=self)

                self.record_timing(task, result, configuration, all_keywords)

                if not result.ok:
                    reason = result.reason or "unknown"
                    if result.returncode is None or reason.startswith(
                        "attempts exhausted"
                    ):
                        # It did not run, so there is no output to use.
                        self.logger.error(
                            f"There was an error running MOPAC: {reason}\n"
                            + result.stderr
                        )
                        return None
                    self.logger.warning(f"MOPAC failed: {reason}\n" + result.stderr)

                self.logger.debug("\n" + pprint.pformat(result))

                self.logger.debug(
                    "\n\nOutput from MOPAC\n\n"
                    + str(result.files.get("mopac.out", ""))
                    + "\n\n"
                )

        # Ran successfully, put out the success file
        (directory / "success.dat").write_text("success")

        if not self.input_only:
            # Analyze the results
            self.analyze(n_calculations=n_calculations, output=output)

        # Close the reference handler, which should force it to close the
        # connection.
        self.references = None

        return next_node

    def record_timing(self, task, result, configuration, keyword_lines):
        """Append this run's timing record (``~/.seamm.d/timing/mopac.csv``):
        the common columns from the task layer, the descriptors from
        :func:`timing_descriptors`. Never raises; a restored result is not
        recorded."""
        try:
            if result.restored:
                return
            text = result.files.get("mopac.out")
            if text is None:
                path = Path(self.directory) / "mopac.out"
                text = path.read_text(errors="replace") if path.exists() else None
            if isinstance(text, bytes):
                text = text.decode(errors="replace")
            jobs = job_descriptors(keyword_lines, text, configuration)
            wall = seamm_exec.timing.task_wall_seconds(result)
            if (
                jobs is None
                or wall is None
                or any(j.get("code_seconds") is None for j in jobs)
            ):
                seamm_exec.record_task_timing(
                    task,
                    result,
                    timing_descriptors(keyword_lines, text, configuration),
                    **_record_kwargs(),
                )
                return
            # One record per job. The run's start-up (wall time less MOPAC's
            # own) is given to each, so each looks like the job run alone.
            overhead = max(0.0, wall - sum(j["code_seconds"] for j in jobs))
            resources = getattr(task, "resources", None)
            for d in jobs:
                seamm_exec.record_timing(
                    "mopac",
                    d["code_seconds"] + overhead,
                    d,
                    ntasks=getattr(resources, "ntasks", None),
                    cpus_per_task=getattr(resources, "cpus_per_task", None),
                    mem_per_cpu=getattr(resources, "mem_per_cpu", None),
                    estimated=task.estimated_seconds if d["job"] == 1 else None,
                    state=getattr(result, "state", ""),
                    timed_out=getattr(result, "timed_out", False),
                    attempts=getattr(result, "attempts", None),
                    in_situ=getattr(result, "in_situ", None),
                    **_record_kwargs(),
                )
        except Exception as e:  # pragma: no cover - must never stop the step
            self.logger.warning(f"Could not record the timing of the MOPAC run: {e}")

    def set_id(self, node_id):
        """Set the id for node to a given tuple"""
        # and set our subnodes
        self.subflowchart.set_ids(node_id)

        return super().set_id(node_id)

    def analyze(self, indent="", lines=[], n_calculations=None, output=""):
        """Read the results from MOPAC calculations and analyze them,
        putting key results into variables for subsequent use by
        other stages
        """

        # Split the aux files into sections for each step
        filename = "mopac.aux"
        with open(os.path.join(self.directory, filename), mode="r") as fd:
            lines_aux = fd.read().splitlines()

        # Find the sections in the file corresponding to sub-tasks
        # MOPAC keeps cumulative times, so fix them
        t_total = 0.0
        aux_data = []
        start = 0
        lineno = 0
        section = 0
        for line in lines_aux:
            if "END OF MOPAC FILE" in line or "END OF MOPAC PROGRAM" in line:
                self.logger.debug("\nAUX file section {}".format(section))
                self.logger.debug("------------------")

                tmp_data = self.parse_aux(lines_aux[start:lineno])
                if "CPU_TIME" in tmp_data:
                    tmp = tmp_data["CPU_TIME"]
                    tmp_data["CPU_TIME"] = tmp - t_total
                    t_total = tmp
                aux_data.append(tmp_data)

                self.logger.debug(pprint.pformat(tmp_data, width=170, compact=True))
            lineno += 1
            if "START OF MOPAC FILE" in line:
                section += 1
                start = lineno

        # Split the output file into sections for each step
        filename = "mopac.out"
        with open(os.path.join(self.directory, filename), mode="r") as fd:
            lines = fd.read().splitlines()

        # Find the sections in the file corresponding to sub-tasks
        out = []
        start = 0
        lineno = 0
        for line in lines:
            if "** Cite this program as:" in line or "Digital Object Ident" in line:
                if lineno == 5:
                    continue
                out.append(lines[start : lineno - 5])
                start = lineno - 6
            lineno += 1
        out.append(lines[start:])

        for data in aux_data:
            # Add main citation for MOPAC
            if "MOPAC_VERSION" in data:
                # like MOPAC2016.20.191M
                release, version = data["MOPAC_VERSION"].split(".", maxsplit=1)
                try:
                    t = datetime.strptime(version[0:-1], "%y.%j")
                    year = t.year
                    month = t.month
                    template = string.Template(self._bibliography["Stewart_2016"])
                    month = calendar.month_abbr[int(month)].lower()
                    citation = template.substitute(
                        month=month, version=version, year=year, release=release
                    )
                    self.references.cite(
                        raw=citation,
                        alias="mopac",
                        module="mopac_step",
                        level=1,
                        note="The principle MOPAC citation.",
                    )
                except Exception:
                    self.references.cite(
                        raw=self._bibliography["stewart_james_j_p_2022_6811510"],
                        alias="mopac",
                        module="mopac_step",
                        level=1,
                        note="The principle MOPAC citation.",
                    )
                break

        # Loop through our subnodes. Get the first real node
        node = self.subflowchart.get_node("1").next()
        first = 0
        n_node = 0
        while node:
            # Print the header for the node
            for value in node.description:
                printer.normal(value)
                if output != "":
                    printer.normal(output)
                    printer.normal("")
                    output = ""

            last = first + n_calculations[n_node]
            if last > len(out):
                logger.error("Could not find the MOPAC output for subjob {last + 1}/")
                node.analyze(data_sections=aux_data[first:last], out_sections=[])
            else:
                node.analyze(
                    data_sections=aux_data[first:last], out_sections=out[first:last]
                )
            first = last

            printer.normal("")

            node = node.next()
            n_node += 1

        if n_node > 1 and "CPU_TIME" in aux_data[-1]:
            text = f"MOPAC took a total of {t_total:.2f} s."
            printer.normal(str(__(text, **data, indent=self.indent)))
