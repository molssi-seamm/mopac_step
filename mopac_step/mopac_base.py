# -*- coding: utf-8 -*-

"""Setup and run MOPAC"""

import logging
import re

import seamm
import seamm_util.printing as printing
import mopac_step

logger = logging.getLogger(__name__)
job = printing.getPrinter()
printer = printing.getPrinter("mopac")


class MOPACBase(seamm.Node):
    def __init__(
        self,
        flowchart=None,
        namespace=None,
        extension=None,
        title=None,
        logger=logger,
    ):
        """Initialize the node"""

        logger.debug("Creating MOPACBase {}".format(self))

        super().__init__(
            flowchart=flowchart, title=title, extension=extension, logger=logger
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
        parser = self.flowchart.parser

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
            default="mopac",
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

    def mopac_structure(self):
        """Create the input for the structure."""
        _, configuration = self.get_system_configuration(None)

        structure = ""
        atoms = configuration.atoms
        elements = atoms.symbols
        coordinates = atoms.get_coordinates(fractionals=False)
        if "freeze" in atoms:
            freeze = atoms["freeze"]
        else:
            freeze = [""] * len(elements)
        for element, xyz, frz in zip(elements, coordinates, freeze):
            x, y, z = xyz
            line = "{:2} {: 12.8f} {:d} {: 12.8f} {:d} {: 12.8f} {:d}\n".format(
                element,
                x,
                0 if "x" in frz else 1,
                y,
                0 if "y" in frz else 1,
                z,
                0 if "z" in frz else 1,
            )
            structure += line

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
                    f"{z: 12.8f} {frz}\n"
                )
                structure += line

        return structure

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

        properties = mopac_step.metadata["results"]
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
            if "END OF MOPAC PROGRAM" in line:
                continue
            if "END OF MOPAC FILE" in line:
                continue
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
                    if (
                        name in properties
                        and properties[name]["dimensionality"] == "scalar"
                    ):
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
