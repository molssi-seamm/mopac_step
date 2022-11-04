# -*- coding: utf-8 -*-

"""Run a thermodynamics calculation in MOPAC"""

import csv
import logging
from pathlib import Path
import textwrap
import traceback

from tabulate import tabulate

import mopac_step
import seamm
import seamm_util.printing as printing
from seamm_util import Q_, units_class
from seamm_util.printing import FormattedText as __

logger = logging.getLogger(__name__)
job = printing.getPrinter()
printer = printing.getPrinter("mopac")


class Thermodynamics(mopac_step.Energy):
    def __init__(self, flowchart=None, title="Thermodynamics", extension=None):
        """Initialize the node"""

        logger.debug("Creating Thermodynamics {}".format(self))

        super().__init__(flowchart=flowchart, title=title, extension=extension)

        self._calculation = "thermodynamics"
        self._model = None
        self._metadata = mopac_step.metadata
        self.parameters = mopac_step.ThermodynamicsParameters()

        # Customize the options for naming the configuration
        p = self.parameters["configuration name"]
        enumeration = (
            "use SMILES string",
            "use Canonical SMILES string",
            "keep current name",
            "vibrations with <Hamiltonian>",
            "use configuration number",
        )
        p.default = "vibrations with <Hamiltonian>"
        if p.value in p._data["enumeration"] and p.value not in enumeration:
            p.value = p.default
        p._data["enumeration"] = enumeration

        self.description = "Thermodynamic functions"

    def description_text(self, P=None):
        """Prepare information about what this node will do"""

        if not P:
            P = self.parameters.values_to_dict()

        # The energy part of the description
        tmp = super().description_text(P)
        energy_description = textwrap.dedent("\n".join(tmp.splitlines()[1:]))

        text = "Thermodynamics calculation using {hamiltonian}, converged to "
        # Convergence
        if P["convergence"] == "normal":
            text += "the 'normal' level of 1.0e-04 kcal/mol."
        elif P["convergence"] == "precise":
            text += "the 'precise' level of 1.0e-06 kcal/mol."
        elif P["convergence"] == "relative":
            text += "a factor of {relative} times the " "normal criterion."
        elif P["convergence"] == "absolute":
            text += "converged to {absolute}."

        text += (
            "\nThe thermodynamics functions will be calculated from "
            "{Tmin} to {Tmax} in steps of {Tstep}. {trans} lowest "
            "modes will be ignored to approximately account for {trans} "
            "internal rotations.\n\n"
        )

        # Put in the description of the energy calculation
        text += "\n\nThe energy and forces will be c" + energy_description[1:]
        text += "\n\n"

        # Structure handling
        text += "The structure in the standard orientation will {structure handling} "

        confname = P["configuration name"]
        if confname == "use SMILES string":
            text += "using SMILES as its name."
        elif confname == "use Canonical SMILES string":
            text += "using canonical SMILES as its name."
        elif confname == "keep current name":
            text += "keeping the current name."
        elif confname == "vibrations with <Hamiltonian>":
            text += "with 'vibrations with {hamiltonian}' as its name."
        elif confname == "use configuration number":
            text += "using the index of the configuration (1, 2, ...) as its name."
        else:
            confname = confname.replace("<Hamiltonian>", P["hamiltonian"])
            text += f"with '{confname}' as its name."

        return self.header + "\n" + __(text, **P, indent=4 * " ").__str__()

    def get_input(self):
        """Get the input for thermodynamics in MOPAC"""

        P = self.parameters.current_values_to_dict(
            context=seamm.flowchart_variables._data
        )

        # Have to fix formatting for printing...
        PP = dict(P)
        for key in PP:
            if isinstance(PP[key], units_class):
                PP[key] = "{:~P}".format(PP[key])

        # Save the description for later printing
        self.description = []
        self.description.append(__(self.description_text(PP), **PP, indent=self.indent))

        # Convert values with units to the right units, and remove
        # the unit string.
        for key in ("Tmax", "Tmin", "Tstep"):
            P[key] = P[key].to("K").magnitude

        # Remove the 1SCF keyword from the energy setup
        inputs = super().get_input()
        keywords, _, _ = inputs[0]
        if "1SCF" in keywords:
            keywords.remove("1SCF")
        keywords.append("THERMO=({Tmin},{Tmax},{Tstep})".format(**P))
        keywords.append("TRANS={trans}".format(**P))

        return inputs

    def analyze(self, indent="", data_sections=[], out_sections=[], table=None):
        """Parse the output and generating the text output and store the
        data in variables for other stages to access
        """
        # Update the structure
        P = self.parameters.current_values_to_dict(
            context=seamm.flowchart_variables._data
        )

        # Get the data.
        data = data_sections[0]

        if "ORIENTATION_ATOM_X" in data:
            system, starting_configuration = self.get_system_configuration(None)
            periodicity = starting_configuration.periodicity
            if (
                "structure handling" in P
                and P["structure handling"] == "be put in a new configuration"
            ):
                configuration = system.create_configuration(
                    periodicity=periodicity,
                    atomset=starting_configuration.atomset,
                    bondset=starting_configuration.bondset,
                    cell_id=starting_configuration.cell_id,
                )
                configuration.charge = starting_configuration.charge
                configuration.spin_multiplicity = (
                    starting_configuration.spin_multiplicity
                )
            else:
                configuration = starting_configuration

            if periodicity != 0:
                raise NotImplementedError(
                    "Thermodynamics cannot yet handle periodicity"
                )
            xyz = []
            it = iter(data["ORIENTATION_ATOM_X"])
            for x in it:
                xyz.append([float(x), float(next(it)), float(next(it))])
            configuration.atoms.set_coordinates(xyz, fractionals=False)

            # And the name of the configuration.
            if "configuration name" in P:
                if P["configuration name"] == "use SMILES string":
                    configuration.name = configuration.smiles
                elif P["configuration name"] == "use Canonical SMILES string":
                    configuration.name = configuration.canonical_smiles
                elif P["configuration name"] == "keep current name":
                    pass
                elif P["configuration name"] == "vibrations with <Hamiltonian>":
                    configuration.name = f"vibrations with {P['hamiltonian']}"
                else:
                    confname = P["configuration name"]
                    confname = confname.replace("<Hamiltonian>", P["hamiltonian"])
                    configuration.name = confname

        # Write the structure out for viewing.
        directory = Path(self.directory)
        directory.mkdir(parents=True, exist_ok=True)

        #  MMCIF file has bonds
        try:
            path = directory / "optimized.mmcif"
            path.write_text(configuration.to_mmcif_text())
        except Exception:
            message = "Error creating the mmcif file\n\n" + traceback.format_exc()
            logger.warning(message)
        # CIF file has cell
        if configuration.periodicity == 3:
            try:
                path = directory / "optimized.cif"
                path.write_text(configuration.to_cif_text())
            except Exception:
                message = "Error creating the cif file\n\n" + traceback.format_exc()
                logger.warning(message)

        # Print the moments of inertia
        p1, p2, p3 = data["PRI_MOM_OF_I"]
        r1, r2, r3 = data["ROTAT_CONSTS"]
        tbl = {
            "Property": ("Principal moment of inertia", "Rotational constants"),
            "1": (p1, r1),
            "2": (p2, r2),
            "3": (p3, r3),
            "Units": ("1.0E-40 g.cm^2", "1/cm"),
        }
        text_lines = "                  Rotational Constants\n"
        text_lines += tabulate(
            tbl,
            headers="keys",
            tablefmt="psql",
            colalign=("center", "decimal", "decimal", "decimal", "left"),
        )
        text_lines += "\n\n"

        # Print the thermodynamic functions and dump to a csv file
        thermo_tbl = {
            "T (K)": data["THERMODYNAMIC_PROPERTIES_TEMPS"],
            "Hv (cal/mol)": data["ENTHALPY_TOT"],
            "Cv (cal/mol/K)": data["HEAT_CAPACITY_TOT"],
            "Sv (cal/mol/K)": data["ENTROPY_TOT"],
            "Hf (kcal/mol)": data["H_O_F(T)"],
        }
        text_lines += "                  Thermodynamic Functions\n"
        text_lines += tabulate(
            thermo_tbl,
            headers="keys",
            tablefmt="psql",
        )
        text_lines += "\n"
        text = textwrap.indent(text_lines, self.indent + 7 * " ")
        printer.normal(text)

        with open(directory / "thermodynamics.csv", "w", newline="") as fd:
            writer = csv.writer(fd)
            writer.writerow(thermo_tbl.keys())
            for row in zip(
                data["THERMODYNAMIC_PROPERTIES_TEMPS"],
                data["ENTHALPY_TOT"],
                data["HEAT_CAPACITY_TOT"],
                data["ENTROPY_TOT"],
                data["H_O_F(T)"],
            ):
                writer.writerow(row)

        # And the vibrational modes to a csv file
        # First, how many rotations are there?
        n_rot = sum([0 if PMI < 0.001 else 1 for PMI in data["PRI_MOM_OF_I"]])
        n_vib = len(data["VIB._FREQ"]) - 3 - n_rot
        with open(directory / "vibrations.csv", "w", newline="") as fd:
            writer = csv.writer(fd)
            writer.writerow(
                (
                    "Mode",
                    "Frequency (1/cm)",
                    "Symmetry",
                    "Transition Dipole (e-)",
                    "Travel (Å)",
                    "Reduced Mass (amu)",
                    "Effective Mass (amu)",
                )
            )
            for row in zip(
                range(1, n_vib + 1),
                data["VIB._FREQ"][0:n_vib],
                data["NORMAL_MODE_SYMMETRY_LABELS"][0:n_vib],
                data["VIB._T_DIP"][0:n_vib],
                data["VIB._TRAVEL"][0:n_vib],
                data["VIB._RED_MASS"][0:n_vib],
                data["VIB._EFF_MASS"][0:n_vib],
            ):
                writer.writerow(row)

        # Add the zero point energy to the results table
        if table is None:
            table = {
                "Property": [],
                "Value": [],
                "Units": [],
            }

        if "ZERO_POINT_ENERGY" in data:
            tmp = data["ZERO_POINT_ENERGY"]
            table["Property"].append("Zero-Point Energy")
            table["Value"].append(f"{tmp:.2f}")
            table["Units"].append("kcal/mol")

            tmp = Q_(tmp, "kcal/mol").to("kJ/mol").magnitude
            table["Property"].append("")
            table["Value"].append(f"{tmp:.2f}")
            table["Units"].append("kJ/mol")

        # Let the energy module do its thing
        super().analyze(
            indent=indent,
            data_sections=data_sections,
            out_sections=out_sections,
            table=table,
        )
