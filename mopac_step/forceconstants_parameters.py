# -*- coding: utf-8 -*-

"""Control parameters for a MOPAC vibrational (Forceconstants/Raman) calculation"""

import logging
import mopac_step

logger = logging.getLogger(__name__)


class ForceconstantsParameters(mopac_step.EnergyParameters):
    """The control parameters for creating a structure from SMILES"""

    parameters = {
        "what": {
            "default": "full Hessian",
            "kind": "enum",
            "default_units": "",
            "enumeration": ("full Hessian", "atom part only", "cell part only"),
            "format_string": "",
            "group": "",
            "description": "Output:",
            "help_text": "What part(s) of the Hessian to output",
        },
        "stepsize": {
            "default": "0.01",
            "kind": "float",
            "default_units": "",
            "enumeration": tuple(),
            "format_string": ".3f",
            "description": "Strain step size:",
            "help_text": (
                "The step size to use straining the system in the finite difference "
                "step."
            ),
        },
        "two-sided_atoms": {
            "default": "no",
            "kind": "boolean",
            "default_units": "",
            "enumeration": ("yes", "no"),
            "format_string": "",
            "group": "",
            "description": "Two-sided atom displacements:",
            "help_text": (
                "Whether to use two-sided finite differences for atom portion."
            ),
        },
        "two-sided_cell": {
            "default": "yes",
            "kind": "boolean",
            "default_units": "",
            "enumeration": ("yes", "no"),
            "format_string": "",
            "group": "",
            "description": "Two-sided strain differences:",
            "help_text": (
                "Whether to use two-sided finite differences for cell portion."
            ),
        },
        "atom_units": {
            "default": "N/m",
            "kind": "str",
            "default_units": "",
            "enumeration": ("N/m", "kJ/mol/Å^2", "kcal/mol/Å^2", "eV/Å^2"),
            "format_string": "",
            "group": "",
            "description": "Units for atom part:",
            "help_text": (
                "What units to use for the atom-atom and atom-cell parts of the Hessian"
            ),
        },
        "cell_units": {
            "default": "GPa",
            "kind": "str",
            "default_units": "",
            "enumeration": ("GPa", "atm"),
            "format_string": "",
            "group": "",
            "description": "Units for cell part:",
            "help_text": "What units to use for the cell-cell part of the Hessian",
        },
    }

    def __init__(self, defaults={}, data=None):
        """Initialize the instance, by default from the default
        parameters given in the class"""

        super().__init__(
            defaults={
                **ForceconstantsParameters.parameters,
                **defaults,
            },
            data=data,
        )

        # Do any local editing of defaults
        tmp = self["system name"]
        tmp._data["enumeration"] = (*tmp.enumeration, "MOPAC standard orientation")
        tmp.default = "keep current name"

        tmp = self["configuration name"]
        tmp._data["enumeration"] = ["MOPAC standard orientation", *tmp.enumeration]
        tmp.default = "MOPAC standard optimization"
