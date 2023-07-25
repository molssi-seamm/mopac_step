# -*- coding: utf-8 -*-

"""Setup and run MOPAC for the Lewis structure"""

import calendar
import datetime
import json  # noqa: F401
import logging
from pathlib import Path
import pprint
import os
import string
import textwrap

from tabulate import tabulate

import mopac_step
import seamm
import seamm_util
import seamm_util.printing as printing
from seamm_util.printing import FormattedText as __

# from seamm_util.printing import FormattedText as __


logger = logging.getLogger(__name__)
job = printing.getPrinter()
printer = printing.getPrinter("mopac")


class LewisStructure(mopac_step.MOPACBase):
    def __init__(self, flowchart=None, extension=None):
        """Initialize the node"""

        logger.debug("Creating MOPAC {}".format(self))

        super().__init__(
            flowchart=flowchart,
            title="Lewis Structure",
            extension=extension,
            logger=logger,
        )

        self._calculation = "Lewis structure"
        self._model = None
        self._metadata = {**mopac_step.metadata}
        # Don't want user to change keywords!
        del self._metadata["keywords"]
        self.parameters = mopac_step.LewisStructureParameters()
        self._lattice_opt = False

    def description_text(self, P=None):
        """Return a short description of this step.

        Return a nicely formatted string describing what this step will
        do.

        Keyword arguments:
            P: a dictionary of parameter values, which may be variables
                or final values. If None, then the parameters values will
                be used as is.
        """
        if not P:
            P = self.parameters.values_to_dict()

        if P["use bonds"]:
            text = (
                "Generate and print the Lewis structure and replace any existing bonds "
                "with those from the Lewis structure."
            )
        else:
            text = "Generate and print the Lewis structure."

        return self.header + "\n" + __(text, **P, indent=4 * " ").__str__()

    def run(self):
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

        if options["mopac_path"] == "":
            mopac_exe = seamm_util.check_executable(options["mopac_exe"])
        else:
            mopac_exe = (
                Path(options["mopac_path"]).expanduser().resolve()
                / options["mopac_exe"]
            )
        mopac_path = Path(mopac_exe).parent.expanduser().resolve()

        env = {
            "LD_LIBRARY_PATH": str(mopac_path),
            "OMP_NUM_THREADS": "1",
        }

        extra_keywords = ["AUX(MOS=10,XP,XS,PRECISION=3)"]

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

        # Always add the charge since that will cause MOZYME, if used, to check.
        extra_keywords.append(f"CHARGE={configuration.charge}")
        # Sparkles affect the number of electrons .. each has 3? .. so ignore
        # multiplicity
        if False:
            # if "SPARKLES" not in extra_keywords:
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

        next_node = super().run(printer)

        text = ""
        lines = []
        lines.append(" ".join(["LEWIS", "LET", "GEO-OK"] + extra_keywords))
        lines.append(system.name)
        lines.append(configuration.name)

        text += "\n".join(lines)
        text += "\n"
        text += self.mopac_structure()
        text += "\n"

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
        self.analyze()

        # Close the reference handler, which should force it to close the
        # connection.
        self.references = None

        return next_node

    def analyze(self, indent="", lines=[], n_calculations=None):
        """Read the results from the Lewis calculation and process."""
        _, configuration = self.get_system_configuration(None)

        # Split the aux files into sections for each step
        filename = "mopac.aux"
        with open(os.path.join(self.directory, filename), mode="r") as fd:
            lines_aux = fd.read().splitlines()
        data = self.parse_aux(lines_aux[2:-1])

        # Add main citation for MOPAC
        if "MOPAC_VERSION" in data:
            # like MOPAC2016.20.191M
            if data["MOPAC_VERSION"][0:5] == "MOPAC":
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
            else:
                self.references.cite(
                    raw=self._bibliography["stewart_james_j_p_2022_6811510"],
                    alias="mopac",
                    module="mopac_step",
                    level=1,
                    note="The principle MOPAC citation.",
                )
        else:
            self.references.cite(
                raw=self._bibliography["stewart_james_j_p_2022_6811510"],
                alias="mopac",
                module="mopac_step",
                level=1,
                note="The principle MOPAC citation.",
            )

        # Get the output file
        filename = "mopac.out"
        with open(os.path.join(self.directory, filename), mode="r") as fd:
            lines = iter(fd.read().splitlines())

        # Get the parameters used
        P = self.parameters.current_values_to_dict(
            context=seamm.flowchart_variables._data
        )
        no_error = P["ignore errors"]
        fallback = P["on errors use connectivity"]

        charge = None
        n_atoms = configuration.n_atoms
        point_group = None
        neighbors = data["neighbors"] = [[] for i in range(n_atoms)]
        bonds = data["bonds"] = {"i": [], "j": [], "bondorder": []}
        lone_pairs = data["lone pairs"] = [0] * n_atoms
        have_lewis_structure = False
        for line in lines:
            line = line.strip()
            if "MOLECULAR POINT GROUP" in line:
                point_group = line.split()[-1]

            if "COMPUTED CHARGE ON SYSTEM" in line:
                charge = int(line.split()[4].rstrip(","))
                if "THIS IS THE SAME AS THE CHARGE DEFINED" not in line:
                    if no_error or fallback:
                        self.logger.warning(
                            f"The charge on the system {configuration.charge} is not "
                            f"the same as Lewis structure indicates: {charge}"
                        )
                    else:
                        raise RuntimeError(
                            f"The charge on the system {configuration.charge} is not "
                            f"the same as Lewis structure indicates: {charge}"
                        )
            if "TOPOGRAPHY OF SYSTEM" in line:
                next(lines)
                next(lines)
                for line in lines:
                    line = line.strip()
                    if line == "":
                        break
                    tmp = line.split()
                    if len(tmp) > 2:
                        i = int(tmp[0]) - 1
                        if i < 0 or i >= n_atoms:
                            raise RuntimeError(
                                f"Problem with atom index in topography {n_atoms=}: "
                                f"{line}"
                            )
                        neighbors[i] = [int(j) - 1 for j in tmp[2:]]

            if line == "Lewis Structure":
                have_lewis_structure = True
                next(lines)
                next(lines)
                tmp_bonds = {}
                for line in lines:
                    if line.strip() == "":
                        break
                    for start in range(1, 4 * 24, 24):
                        tmp = line[start : start + 24].strip().split()
                        if len(tmp) == 3:
                            i = int(tmp[1]) - 1
                            j = int(tmp[2]) - 1
                            if j < i:
                                i, j = j, i
                            key = f"{i}-{j}"
                            if key in tmp_bonds:
                                tmp_bonds[key] += 1
                            else:
                                tmp_bonds[key] = 1
                        elif len(tmp) == 2:
                            i = int(tmp[1]) - 1
                            lone_pairs[i] += 1
                for key, order in tmp_bonds.items():
                    i, j = key.split("-")
                    bonds["i"].append(int(i))
                    bonds["j"].append(int(j))
                    bonds["bondorder"].append(order)

                # The neighbors according to Lewis structure
                lneighbors = [[] for i in range(n_atoms)]
                for i, j in zip(bonds["i"], bonds["j"]):
                    lneighbors[i].append(j)
                    lneighbors[j].append(i)

        if charge is not None:
            data["charge"] = charge
        if point_group is not None:
            data["point group"] = point_group

        self.logger.debug(f"Point group = {point_group}")
        self.logger.debug(f"     Charge = {charge}")
        self.logger.debug("Neighbors")
        self.logger.debug(json.dumps(neighbors, indent=4))
        self.logger.debug("Bonds")
        self.logger.debug(json.dumps(bonds, indent=4))
        self.logger.debug("Lone pairs")
        self.logger.debug(json.dumps(lone_pairs, indent=4))

        # Check the Lewis structure for consistency with neighbors.
        same = False
        if have_lewis_structure:
            same = True
            for i in range(n_atoms):
                if sorted(neighbors[i]) != sorted(lneighbors[i]):
                    same = False
                    break

            if not same:
                if no_error:
                    self.logger.warning(
                        "The Lewis structure yields different connectivity than the "
                        "simple connectivity."
                    )
                elif not fallback:
                    raise RuntimeError(
                        "The Lewis structure yields different connectivity than the "
                        "simple connectivity shows."
                    )

        # Generate the printed output if requested
        text = ""
        if P["atom cutoff"] != "no printing":
            text += f"Point group symmetry: {point_group}\n"
            text += f"          Net charge: {charge}\n"

        if P["atom cutoff"] == "no printing":
            pass
        elif P["atom cutoff"] == "unlimited" or P["atom cutoff"] >= n_atoms:
            symbol = configuration.atoms.symbols
            nmax = 0
            for atoms in neighbors:
                if len(atoms) > nmax:
                    nmax = len(atoms)
            table = {"Atom": [], "El": [], "Lone Pairs": []}
            for i in range(1, nmax + 1):
                table[f"At{i}"] = []
                table[f"El{i}"] = []
            for i, atoms in enumerate(neighbors):
                table["Atom"].append(i + 1)
                table["El"].append(symbol[i])
                table["Lone Pairs"].append(lone_pairs[i])
                for c, j in enumerate(atoms, start=1):
                    table[f"At{c}"].append(j + 1)
                    table[f"El{c}"].append(symbol[j])
                for c in range(len(atoms) + 1, nmax + 1):
                    table[f"At{c}"].append("")
                    table[f"El{c}"].append("")
            tmp = tabulate(table, headers="keys", tablefmt="pretty")
            length = len(tmp.splitlines()[0])
            text += "\n"
            text += "Atoms bonded to each atom".center(length)
            text += "\n"
            text += tmp
            text += "\n"
            text += "\n"

            table = {
                "At1": [i + 1 for i in bonds["i"]],
                "At2": [j + 1 for j in bonds["j"]],
            }
            txt = table["Bond"] = []
            for i, j, order in zip(bonds["i"], bonds["j"], bonds["bondorder"]):
                el1 = symbol[i]
                el2 = symbol[j]
                if order == 1:
                    txt.append(f"{el1}-{el2}")
                elif order == 2:
                    txt.append(f"{el1}={el2}")
                elif order == 3:
                    txt.append(f"{el1}#{el2}")
                else:
                    txt.append(f"{el1}-{order}-{el2}")
            tmp = tabulate(table, headers="keys", tablefmt="pretty")
            length = len(tmp.splitlines()[0])
            text += "\n"
            text += "Bonds".center(length)
            text += "\n"
            text += tmp
            text += "\n"

        # If requested, overwrite the bonding information in the system
        if P["use bonds"]:
            ids = configuration.atoms.ids
            if same:
                iatoms = [ids[i] for i in bonds["i"]]
                jatoms = [ids[j] for j in bonds["j"]]
                configuration.bonds.delete()
                configuration.bonds.append(
                    i=iatoms, j=jatoms, bondorder=bonds["bondorder"]
                )
                text += "\nReplaced the bonds in the configuration with those from the "
                text += "Lewis structure.\n"
            else:
                iatoms = []
                jatoms = []
                bondorders = []
                for i in range(n_atoms):
                    for j in lneighbors[i]:
                        if j > i:
                            iatoms.append(ids[i])
                            jatoms.append(ids[j])
                            bondorders.append(1)
                configuration.bonds.delete()
                configuration.bonds.append(
                    i=iatoms, j=jatoms, bondorder=bonds["bondorder"]
                )
                text += "\nReplaced the bonds in the configuration with those from the "
                text += "simple connectivity structure.\n"

        # Put any requested results into variables or tables
        self.store_results(
            configuration=configuration,
            data=data,
        )

        if "CPU_TIME" in data:
            t_total = data["CPU_TIME"]
            text += f"\nThe Lewis structure took a total of {t_total:.2f} s.\n"

        printer.normal(textwrap.indent(text, self.indent + 4 * " "))
