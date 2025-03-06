# -*- coding: utf-8 -*-

"""Setup and run MOPAC"""

import calendar
import configparser
import csv
from datetime import datetime, timezone
import importlib
import logging
import os
import os.path
from pathlib import Path
import platform
import pprint
import shutil
import string
import time

from cpuinfo import get_cpu_info

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
        self._input_only = False

        super().__init__(
            flowchart=flowchart, title=title, extension=extension, logger=logger
        )

        # Set up the timing information
        self._timing_data = []
        self._timing_path = Path("~/.seamm.d/timing/mopac.csv").expanduser()
        self._timing_header = [
            "node",  # 0
            "cpu",  # 1
            "cpu_version",  # 2
            "cpu_count",  # 3
            "cpu_speed",  # 4
            "date",  # 5
            "H_SMILES",  # 6
            "ISOMERIC_SMILES",  # 7
            "formula",  # 8
            "net_charge",  # 9
            "spin_multiplicity",  # 10
            "keywords",  # 11
            "nproc",  # 12
            "time",  # 13
        ]
        try:
            self._timing_path.parent.mkdir(parents=True, exist_ok=True)

            self._timing_data = 14 * [""]
            self._timing_data[0] = platform.node()
            tmp = get_cpu_info()
            if "arch" in tmp:
                self._timing_data[1] = tmp["arch"]
            if "cpuinfo_version_string" in tmp:
                self._timing_data[2] = tmp["cpuinfo_version_string"]
            if "count" in tmp:
                self._timing_data[3] = str(tmp["count"])
            if "hz_advertized_friendly" in tmp:
                self._timing_data[4] = tmp["hz_advertized_friendly"]

            if not self._timing_path.exists():
                with self._timing_path.open("w", newline="") as fd:
                    writer = csv.writer(fd)
                    writer.writerow(self._timing_header)
        except Exception:
            self._timing_data = None

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
                        text += self.mopac_structure()
                        text += "\n"
                else:
                    text += structure
                    text += "\n"
            node = node.next()

        # Check for successful run, don't rerun
        output = ""  # Text output to print
        success = directory / "success.dat"
        if success.exists():
            self._timing_data = None
        else:
            # Input files
            files = {"mopac.dat": text}
            self.logger.debug("mopac.dat:\n" + files["mopac.dat"])
            for filename in files:
                path = directory / filename
                path.write_text(files[filename])

            if self.input_only:
                self._timing_data = None
            else:
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

                # Use the matching version of the seamm-mopac image by default.
                config["version"] = self.version

                return_files = [
                    "mopac.arc",
                    "mopac.out",
                    "mopac.aux",
                    "stdout.txt",
                    "stderr.txt",
                ]

                if self._timing_data is not None:
                    try:
                        self._timing_data[6] = configuration.to_smiles(
                            canonical=True, hydrogens=True
                        )
                    except Exception:
                        self._timing_data[6] = ""
                    try:
                        self._timing_data[7] = configuration.isomeric_smiles
                    except Exception:
                        self._timing_data[7] = ""
                    try:
                        self._timing_data[8] = configuration.formula[0]
                    except Exception:
                        self._timing_data[7] = ""
                    try:
                        self._timing_data[9] = str(configuration.charge)
                    except Exception:
                        self._timing_data[9] = ""
                    try:
                        self._timing_data[10] = str(configuration.spin_multiplicity)
                    except Exception:
                        self._timing_data[10] = ""

                    self._timing_data[11] = " && ".join(all_keywords)
                    self._timing_data[5] = datetime.now(timezone.utc).isoformat()

                t0 = time.time_ns()

                result = executor.run(
                    cmd=["{code}", "mopac.dat", ">", "stdout.txt", "2>", "stderr.txt"],
                    config=config,
                    directory=self.directory,
                    files=files,
                    return_files=return_files,
                    in_situ=True,
                    shell=True,
                    env=env,
                )

                t = (time.time_ns() - t0) / 1.0e9
                if self._timing_data is not None:
                    self._timing_data[13] = f"{t:.3f}"
                    self._timing_data[12] = str(n_cores)
                    try:
                        with self._timing_path.open("a", newline="") as fd:
                            writer = csv.writer(fd)
                            writer.writerow(self._timing_data)
                    except Exception:
                        pass

                if not result:
                    self.logger.error("There was an error running MOPAC")
                    return None

                self.logger.debug("\n" + pprint.pformat(result))

                self.logger.debug(
                    "\n\nOutput from MOPAC\n\n" + result["mopac.out"]["data"] + "\n\n"
                )

        # Ran successfully, put out the success file
        success.write_text("success")

        if not self.input_only:
            # Analyze the results
            self.analyze(n_calculations=n_calculations, output=output)

        # Close the reference handler, which should force it to close the
        # connection.
        self.references = None

        return next_node

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
