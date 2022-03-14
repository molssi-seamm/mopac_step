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
    }

    def __init__(self, defaults={}, data=None):
        """Initialize the instance, by default from the default
        parameters given in the class"""

        super().__init__(
            defaults={
                **IRParameters.parameters,
                **mopac_step.structure_handling_parameters,
                **defaults,
            },
            data=data,
        )
