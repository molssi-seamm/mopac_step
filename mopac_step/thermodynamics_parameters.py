# -*- coding: utf-8 -*-
"""Control parameters for a MOPAC thermodynamics calculation
"""

import logging
import mopac_step

logger = logging.getLogger(__name__)


class ThermodynamicsParameters(mopac_step.EnergyParameters):
    """The control parameters for creating a structure from SMILES"""

    parameters = {
        "Tmin": {
            "default": "200",
            "kind": "float",
            "default_units": "K",
            "enumeration": tuple(),
            "format_string": ".1f",
            "description": "Minimum temperature:",
            "help_text": (
                "The minimum temperature for the thermodynamic " "functions."
            ),
        },
        "Tmax": {
            "default": "400",
            "kind": "float",
            "default_units": "K",
            "enumeration": tuple(),
            "format_string": ".1f",
            "description": "Maximum temperature:",
            "help_text": (
                "The maximum temperature for the thermodynamic " "functions."
            ),
        },
        "Tstep": {
            "default": "10",
            "kind": "float",
            "default_units": "K",
            "enumeration": tuple(),
            "format_string": ".1f",
            "description": "Temperature interval:",
            "help_text": (
                "The interval between temperatures for the " "thermodynamic functions."
            ),
        },
        "trans": {
            "default": "0",
            "kind": "integer",
            "default_units": "",
            "enumeration": tuple(),
            "format_string": "d",
            "description": "Number of internal rotations to ignore:",
            "help_text": (
                "The number of internal rotations to ignore. "
                "A corresponding number of the lowest modes "
                "will be ignored, which is a first approximation."
            ),
        },
        # Put in the configuration handling options needed
        "structure handling": {
            "default": "Overwrite the current configuration",
            "kind": "enum",
            "default_units": "",
            "enumeration": (
                "Overwrite the current configuration",
                "Create a new configuration",
            ),
            "format_string": "s",
            "description": "Configuration handling:",
            "help_text": (
                "Whether to overwrite the current configuration, or create a new "
                "configuration or system and configuration for the new structure"
            ),
        },
        "configuration name": {
            "default": "vibrations with <Hamiltonian>",
            "kind": "string",
            "default_units": "",
            "enumeration": (
                "vibrations with <Hamiltonian>",
                "keep current name",
                "use SMILES string",
                "use Canonical SMILES string",
                "use configuration number",
            ),
            "format_string": "s",
            "description": "Configuration name:",
            "help_text": "The name for the new configuration",
        },
    }

    def __init__(self, defaults={}, data=None):
        """Initialize the instance, by default from the default
        parameters given in the class"""

        super().__init__(
            defaults={**ThermodynamicsParameters.parameters, **defaults}, data=data
        )
