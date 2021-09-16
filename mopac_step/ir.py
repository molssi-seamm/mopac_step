# -*- coding: utf-8 -*-

"""Run a vibrational frequency calculation in MOPAC"""

import logging
import seamm
import seamm_util.printing as printing
from seamm_util import units_class
from seamm_util.printing import FormattedText as __
import mopac_step

logger = logging.getLogger(__name__)
job = printing.getPrinter()
printer = printing.getPrinter("mopac")


class IR(mopac_step.Energy):
    def __init__(self, flowchart=None, title="IR Spectrum", extension=None):
        """Initialize the node"""

        logger.debug("Creating IR {}".format(self))

        super().__init__(flowchart=flowchart, title=title, extension=extension)

        self.parameters = mopac_step.IRParameters()
        self.description = "Infrared (vibrational) spectroscopy calculation"

    def description_text(self, P=None):
        """Prepare information about what this node will do"""

        if not P:
            P = self.parameters.values_to_dict()

        text = (
            "Harmonic vibrational calculation using {hamiltonian}, "
            "with the SCF converged to "
        )
        # Convergence
        if P["convergence"] == "normal":
            text += "the 'normal' level of 1.0e-07 kcal/mol."
        elif P["convergence"] == "precise":
            text += "the 'precise' level of 1.0e-09 kcal/mol."
        elif P["convergence"] == "relative":
            text += "a factor of {relative} times the " "normal criterion."
        elif P["convergence"] == "absolute":
            text += "converged to {absolute}."

        if P["trans"] != 0:
            text += (
                "\n\nA total of {trans} lowest modes will be ignored to "
                "approximately account for {trans} internal rotations."
            )

        # Structure handling
        handling = P["structure handling"]
        text += " The structure in the standard orientation will "
        if handling == "Overwrite the current configuration":
            text += "overwrite the current configuration "
        elif handling == "Create a new configuration":
            text += "be put in a new configuration "
        else:
            raise ValueError(
                f"Do not understand how to handle the structure: '{handling}'"
            )

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
            text += "with '{confname}' as its name."

        return self.header + "\n" + __(text, **P, indent=4 * " ").__str__()

    def get_input(self):
        """Get the input for an optimization MOPAC"""

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

        # Remove the 1SCF keyword from the energy setup
        keywords = []
        for keyword in super().get_input():
            if keyword == "1SCF":
                keywords.append("FORCE")
                if P["trans"] != 0:
                    keywords.append("TRANS={}".format(P["trans"]))
                if P["let"]:
                    keywords.append("LET")
            else:
                keywords.append(keyword)

        return keywords

    def analyze(self, indent="", data={}, out=[]):
        """Parse the output and generating the text output and store the
        data in variables for other stages to access
        """
        # Update the structure
        P = self.parameters.current_values_to_dict(
            context=seamm.flowchart_variables._data
        )
        if "ORIENTATION_ATOM_X" in data:
            system, starting_configuration = self.get_system_configuration(None)
            periodicity = starting_configuration.periodicity
            if (
                "structure handling" in P
                and P["structure handling"] == "Create a new configuration"
            ):
                configuration = system.create_configuration(
                    periodicity=periodicity,
                    atomset=starting_configuration.atomset,
                    bondset=starting_configuration.bondset,
                    cell_id=starting_configuration.cell_id,
                )
            else:
                configuration = starting_configuration

            if periodicity != 0:
                raise NotImplementedError("IR cannot yet handle periodicity")
            xyz = []
            it = iter(data["ORIENTATION_ATOM_X"])
            for x in it:
                xyz.append([float(x), float(next(it)), float(next(it))])
            configuration.atoms.set_coordinates(xyz, fractionals=False)

            # And the name of the configuration.
            if "configuration name" in P:
                if P["configuration name"] == "vibrations with <Hamiltonian>":
                    configuration.name = f"vibrations with {P['hamiltonian']}"
                elif P["configuration name"] == "keep current name":
                    pass
                elif P["configuration name"] == "use SMILES string":
                    configuration.name = configuration.smiles
                elif P["configuration name"] == "use Canonical SMILES string":
                    configuration.name = configuration.canonical_smiles
                elif P["configuration name"] == "use configuration number":
                    configuration.name = str(configuration.n_configurations)

        # The results
        printer.normal(
            __(
                (
                    "The geometry converged in {NUMBER_SCF_CYCLES} "
                    "iterations to a heat of formation of {HEAT_OF_FORMATION} "
                    "kcal/mol."
                ),
                **data,
                indent=self.indent + 4 * " ",
            )
        )

        # Put any requested results into variables or tables
        self.store_results(
            data=data,
            properties=mopac_step.properties,
            results=self.parameters["results"].value,
            create_tables=self.parameters["create tables"].get(),
        )
