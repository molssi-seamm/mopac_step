# -*- coding: utf-8 -*-

"""Setup and run MOPAC"""

import calendar
import datetime
import logging
import os
import os.path
from pathlib import Path
import pkg_resources
import pprint
import string

import psutil

import molsystem
import seamm
import seamm_util
import seamm_util.printing as printing
from seamm_util.printing import FormattedText as __
import mopac_step

logger = logging.getLogger(__name__)
job = printing.getPrinter()
printer = printing.getPrinter("mopac")

# Add MOPAC's properties to the standard properties
path = Path(pkg_resources.resource_filename(__name__, "data/"))
csv_file = path / "properties.csv"
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

        super().__init__(
            flowchart=flowchart, title=title, extension=extension, logger=logger
        )

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
        system, configuration = self.get_system_configuration(None)
        n_atoms = configuration.n_atoms
        if n_atoms == 0:
            self.logger.error("MOPAC run(): there is no structure!")
            raise RuntimeError("MOPAC run(): there is no structure!")

        # Print our header to the main output
        printer.normal(self.header)
        printer.normal("")

        # Access the options and find the executable
        options = self.options
        seamm_options = self.global_options

        if options["mopac_path"] == "":
            mopac_exe = seamm_util.check_executable(options["mopac_exe"])
        else:
            mopac_exe = (
                Path(options["mopac_path"]).expanduser().resolve()
                / options["mopac_exe"]
            )
        mopac_path = Path(mopac_exe).parent.expanduser().resolve()

        # How many processors does this node have?
        n_cores = psutil.cpu_count(logical=False)
        self.logger.info("The number of cores is {}".format(n_cores))

        if seamm_options["ncores"] != "available":
            n_cores = min(n_cores, int(seamm_options["ncores"]))
        # Currently, on the Mac, it is not clear that any parallelism helps
        # much.

        # if options["ncores"] == "default":
        #     # Wild guess!
        #     # mopac_mkl_num_threads = int(pow(n_atoms / 16, 0.3333))
        #     mkl_num_threads = 1
        # else:
        #     if options["mkl_num_threads"] == "default":
        #         mkl_num_threads = n_cores
        #     else:
        #         mkl_num_threads = int(options["mkl_num_threads"])
        # if mkl_num_threads > n_cores:
        #     mkl_num_threads = n_cores
        # elif mkl_num_threads < 1:
        #     mkl_num_threads = 1
        # self.logger.info(f"MKL will use {mkl_num_threads} threads.")

        n_hydrogens = configuration.atoms.get_n_atoms("atno", "==", 1)
        n_basis = (n_atoms - n_hydrogens) * 4 + n_hydrogens
        if options["ncores"] == "default":
            # Since it is the matrix diagonalization, work out rough
            # size of matrix

            # Wild guess!
            mopac_num_threads = int(pow(n_basis / 1000, 3))
            if mopac_num_threads > n_cores:
                mopac_num_threads = n_cores
        else:
            mopac_num_threads = int(options["ncores"])
        if mopac_num_threads > n_cores:
            mopac_num_threads = n_cores
        if mopac_num_threads < 1:
            mopac_num_threads = 1
        self.logger.info(
            f"MOPAC will use {mopac_num_threads} threads for about {n_basis} basis "
            "functions."
        )

        env = {
            "LD_LIBRARY_PATH": str(mopac_path),
            "OMP_NUM_THREADS": str(mopac_num_threads),
        }
        # "MKL_NUM_THREADS": str(mkl_num_threads),

        # extra_keywords = ["AUX(MOS=10,XP,XS)", "NOXYZ"]
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

        next_node = super().run(printer)

        # Get the first real node
        node = self.subflowchart.get_node("1").next()

        text = ""
        n_calculations = []
        while node:
            node.parent = self
            inputs = node.get_input()
            n_calculations.append(len(inputs))
            for keywords, structure, comment in inputs:
                lines = []
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

        files = {"mopac.dat": text}
        self.logger.debug("mopac.dat:\n" + files["mopac.dat"])
        os.makedirs(self.directory, exist_ok=True)
        for filename in files:
            with open(os.path.join(self.directory, filename), mode="w") as fd:
                fd.write(files[filename])
        local = seamm.ExecLocal()
        return_files = ["mopac.arc", "mopac.out", "mopac.aux"]
        result = local.run(
            cmd=[str(mopac_exe), "mopac.dat"],
            files=files,
            return_files=return_files,
            env=env,
            in_situ=True,
            directory=self.directory,
        )

        if not result:
            self.logger.error("There was an error running MOPAC")
            return None

        self.logger.debug("\n" + pprint.pformat(result))

        self.logger.debug(
            "\n\nOutput from MOPAC\n\n" + result["mopac.out"]["data"] + "\n\n"
        )

        # Analyze the results
        self.analyze(n_calculations=n_calculations)

        # Close the reference handler, which should force it to close the
        # connection.
        self.references = None

        return next_node

    def set_id(self, node_id):
        """Set the id for node to a given tuple"""
        # and set our subnodes
        self.subflowchart.set_ids(node_id)

        return super().set_id(node_id)

    def analyze(self, indent="", lines=[], n_calculations=None):
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
                    t = datetime.datetime.strptime(version[0:-1], "%y.%j")
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
