# -*- coding: utf-8 -*-

"""Setup and run MOPAC"""

import calendar
import datetime
import logging
import os
import os.path
from pathlib import Path
import pprint
import re
import string

import psutil

import seamm
import seamm_util
import seamm_util.printing as printing
from seamm_util.printing import FormattedText as __
import mopac_step

logger = logging.getLogger(__name__)
job = printing.getPrinter()
printer = printing.getPrinter("mopac")


class MOPAC(seamm.Node):
    def __init__(
        self, flowchart=None, namespace="org.molssi.seamm.mopac", extension=None
    ):
        """Initialize the node"""

        logger.debug("Creating MOPAC {}".format(self))

        # Create the subflowchart and proceed
        self.subflowchart = seamm.Flowchart(
            name="MOPAC",
            parent=self,
            namespace=namespace,
            directory=flowchart.root_directory,
        )
        self._data = {}
        self._lattice_opt = True

        super().__init__(
            flowchart=flowchart, title="MOPAC", extension=extension, logger=logger
        )

    @property
    def version(self):
        """The semantic version of this module."""
        return mopac_step.__version__

    @property
    def git_revision(self):
        """The git version of this module."""
        return mopac_step.__git_revision__

    def create_parser(self):
        """Setup the command-line / config file parser"""
        parser_name = self.step_type
        parser = seamm_util.getParser()

        # Remember if the parser exists ... this type of step may have been
        # found before
        parser_exists = parser.exists(parser_name)

        # Create the standard options, e.g. log-level
        result = super().create_parser(name=parser_name)

        if parser_exists:
            return result

        # Options for Mopac
        parser.add_argument(
            parser_name,
            "--mopac-exe",
            default="MOPAC2016.exe",
            help="the name of the MOPAC executable",
        )

        parser.add_argument(
            parser_name,
            "--mopac-path",
            default="",
            help="the path to the MOPAC executable",
        )

        parser.add_argument(
            parser_name,
            "--ncores",
            default="default",
            help="How many threads to use in MOPAC",
        )

        parser.add_argument(
            parser_name,
            "--mkl-num-threads",
            default="default",
            help="How many threads to use with MKL in MOPAC",
        )

        parser.add_argument(
            parser_name,
            "--max-atoms-to-print",
            default=25,
            help="Maximum number of atoms to print charges, etc.",
        )

        return result

    def set_id(self, node_id):
        """Set the id for node to a given tuple"""
        self._id = node_id

        # and set our subnodes
        self.subflowchart.set_ids(self._id)

        return self.next()

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

    def run(self):
        """Run MOPAC"""
        system, configuration = self.get_system_configuration(None)
        n_atoms = configuration.n_atoms
        if n_atoms == 0:
            self.logger.error("MOPAC run(): there is no structure!")
            raise RuntimeError("MOPAC run(): there is no structure!")

        # Print our header to the main output
        printer.important(self.header)
        printer.important("")

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
        extra_keywords = ["AUX(MOS=10,XP,XS)"]

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

        input_data = []
        n_calculations = []
        while node:
            node.parent = self
            inputs = node.get_input()
            n_calculations.append(len(inputs))
            for keywords in inputs:
                lines = []
                lines.append(" ".join(keywords + extra_keywords))
                lines.append(system.name)
                lines.append(configuration.name)

                if "OLDGEO" in keywords:
                    input_data.append("\n".join(lines))
                else:
                    tmp_structure = []
                    atoms = configuration.atoms
                    elements = atoms.symbols
                    coordinates = atoms.get_coordinates(fractionals=False)
                    if "freeze" in atoms:
                        freeze = atoms["freeze"]
                    else:
                        freeze = [""] * len(elements)
                    for element, xyz, frz in zip(elements, coordinates, freeze):
                        x, y, z = xyz
                        line = (
                            "{:2} {: 12.8f} {:d} {: 12.8f} {:d} {: 12.8f} {:d}".format(
                                element,
                                x,
                                0 if "x" in frz else 1,
                                y,
                                0 if "y" in frz else 1,
                                z,
                                0 if "z" in frz else 1,
                            )
                        )
                        tmp_structure.append(line)

                    if configuration.periodicity == 3:
                        # The three translation vectors
                        element = "Tv"
                        uvw = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
                        XYZ = configuration.cell.to_cartesians(uvw)
                        frz = 1 if self._lattice_opt else 0
                        for xyz in XYZ:
                            x, y, z = xyz
                            line = (
                                f"{element:2} {x: 12.8f} {frz} {y: 12.8f} {frz} "
                                f"{z: 12.8f} {frz}"
                            )
                            tmp_structure.append(line)

                    input_data.append(
                        "\n".join(lines) + "\n" + "\n".join(tmp_structure) + "\n"
                    )

            node = node.next()

        files = {"mopac.dat": "\n".join(input_data)}
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
        )

        if not result:
            self.logger.error("There was an error running MOPAC")
            return None

        self.logger.debug("\n" + pprint.pformat(result))

        self.logger.debug(
            "\n\nOutput from MOPAC\n\n" + result["mopac.out"]["data"] + "\n\n"
        )

        for filename in result["files"]:
            with open(os.path.join(self.directory, filename), mode="w") as fd:
                if result[filename]["data"] is not None:
                    fd.write(result[filename]["data"])
                else:
                    fd.write(result[filename]["exception"])

        # Analyze the results
        self.analyze(n_calculations=n_calculations)

        # Close the reference handler, which should force it to close the
        # connection.
        self.references = None

        return next_node

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
            if "END OF MOPAC FILE" in line:
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
            if "** Cite this program as:" in line:
                if lineno == 1:
                    continue
                out.append(lines[start : lineno - 1])
                start = lineno - 2
            lineno += 1
        out.append(lines[start:])

        for data in aux_data:
            # Add main citation for MOPAC
            if "MOPAC_VERSION" in data:
                # like MOPAC2016.20.191M
                release, version = data["MOPAC_VERSION"].split(".", maxsplit=1)
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
                break

        # Loop through our subnodes. Get the first real node
        node = self.subflowchart.get_node("1").next()
        first = 0
        n_node = 0
        while node:
            # Print the header for the node
            for value in node.description:
                printer.important(value)

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

    def parse_arc(self, filename="mopac.arc"):
        """Digest the ARC file and get the coordinates.

        Parameters
        ----------
        filename : str
            The name of the ARC file

        Returns
        -------
        coordinates : [n_atoms*[3]]
        """
        xyz = None
        cell_vectors = []
        with open(filename, "r") as fd:
            for line in fd:
                if "FINAL GEOMETRY OBTAINED" in line:
                    xyz = []
                    ii = 0
                    for line in fd:
                        if " &" not in line and " +" not in line and line[0] != "*":
                            ii += 1
                            if ii == 3:
                                break
                    for line in fd:
                        line = line.strip()
                        if line == "":
                            break
                        if line[0] != "*":
                            symbol, x, fx, y, fy, z, fz = line.split()
                            if symbol == "Tv":
                                cell_vectors.append(
                                    [float(x), float(y), float(z)]
                                )  # yapf: disable
                            else:
                                xyz.append([float(x), float(y), float(z)])
        return xyz, cell_vectors

    def parse_aux(self, lines):
        """Digest a section of the aux file"""

        properties = mopac_step.properties
        trans = str.maketrans("Dd", "Ee")

        data = {}
        lineno = -1
        nlines = len(lines)

        spin_polarized = False

        while True:
            lineno += 1
            if lineno >= nlines:
                break
            line = lines[lineno].strip()
            if line[0] == "#":
                continue
            if "=" not in line:
                raise RuntimeError("Problem parsing MOPAC aux file: '" + line + "'")
            key, rest = line.split("=", maxsplit=1)
            if key[-1] == "]":
                name, size = key[0:-1].split("[")
                size = int(size.lstrip("0"))
                if ":" in name:
                    name, units = name.split(":")

                if name not in properties:
                    logger.warning("Property '{}' not recognized.".format(name))
                    kind = "string"
                else:
                    kind = properties[name]["type"]

                if "units" in properties[name]:
                    data[name + ",units"] = properties[name]["units"]

                if name == "NUM_ALPHA_ELECTRONS":
                    spin_polarized = True

                # Bug workaround
                # Sometimes MOPAC does not write out the MO occupancies
                if name == "MOLECULAR_ORBITAL_OCCUPANCIES":
                    tmp_line = lines[lineno + 1].strip()
                    if tmp_line[0].isalpha():
                        continue
                # end of workaround

                # Check for floating point numbers run together
                if kind == "float":
                    values = []
                    for value in rest.split():
                        tmp = value.split(".")
                        if len(tmp) <= 2:
                            values.append(value)
                        else:
                            # Run together ... lets see how many decimals
                            n_decimals = len(tmp[-1])
                            # and before the decimal
                            n_digits = len(tmp[-2]) - n_decimals
                            n = n_digits + 1 + n_decimals
                            n_values = len(tmp) - 1
                            # blanks at front have been stripped, so count back
                            start = 0
                            end = len(value) - (n_values - 1) * n
                            while start < len(value):
                                values.append(value[start:end])
                                start = end
                                end += n
                    tmp = values
                else:
                    tmp = rest.split()

                # AUX file contains alpha and beta orbitals, that's why we are
                # doubling it
                if name == "MICROSTATE_CONFIGURATIONS" and spin_polarized:
                    size = size * 2

                while len(tmp) < size:
                    lineno += 1
                    line = lines[lineno].strip()
                    if line[0] != "#":
                        tmp.extend(line.split())

                if kind == "integer":
                    values = []
                    for value in tmp:
                        values.append(int(value))
                elif kind == "float":
                    values = []
                    for value in tmp:
                        values.append(float(value.translate(trans)))
                else:
                    values = tmp

                if "UPDATED" in name:
                    if name not in data:
                        data[name] = []
                    data[name].append(values)
                else:
                    if properties[name]["dimensionality"] == "scalar":
                        if not (units == "ARBITRARY_UNITS" and name in data):
                            data[name] = values[0]
                    else:
                        data[name] = values
            else:
                if ":" in key:
                    name, units = key.split(":")
                else:
                    name = key

                if name not in properties:
                    logger.warning("Property '{}' not recognized.".format(name))
                    kind = "string"
                else:
                    kind = properties[name]["type"]
                if "units" in properties[name]:
                    data[name + ",units"] = properties[name]["units"]
                if kind == "integer":
                    value = int(rest)
                elif kind == "float":
                    value = float(self._sanitize_value(rest.strip()))
                else:
                    value = rest.strip('"')

                if "UPDATED" in name:
                    if name not in data:
                        data[name] = []
                    data[name].append(value)
                else:
                    data[name] = value

        return data

    def _sanitize_value(self, value):
        regex = r"^([-+]?[.0-9]+)([EeDd]*)([-+][0-9]+)$"
        subs = r"\1E\3"
        ret = float(re.sub(regex, subs, value))
        return ret
