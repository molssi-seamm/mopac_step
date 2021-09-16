# -*- coding: utf-8 -*-

"""Control parameters for a MOPAC vibrational (IR/Raman) calculation
"""

import logging
import mopac_step

logger = logging.getLogger(__name__)


class IRParameters(mopac_step.EnergyParameters):
    """The control parameters for creating a structure from SMILES"""

    parameters = {
        "let": {
            "default": ("no"),
            "kind": ("boolean"),
            "default_units": (""),
            "enumeration": ("yes", "no"),
            "format_string": (""),
            "group": (""),
            "description": ("Use structure even if not a minimum:"),
            "help_text": (
                "Don't stop if the initial structure is not "
                "a minimum or other stationary point."
            ),
        },
        "trans": {
            "default": ("0"),
            "kind": ("integer"),
            "default_units": (""),
            "enumeration": tuple(),
            "format_string": ("d"),
            "group": (""),
            "description": ("Number of internal rotations to ignore:"),
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

        super().__init__(defaults={**IRParameters.parameters, **defaults}, data=data)
