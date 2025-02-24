# -*- coding: utf-8 -*-
"""Control parameters for a MOPAC single-point energy calculation"""

import logging
import seamm

logger = logging.getLogger(__name__)


class LewisStructureParameters(seamm.Parameters):
    """The control parameters for creating a structure from SMILES"""

    parameters = {
        "atom cutoff": {
            "default": 30,
            "kind": "integer",
            "default_units": "",
            "enumeration": ("no printing", "unlimited"),
            "format_string": "s",
            "description": "No printing if more atoms than:",
            "help_text": "Limit for system size for printing",
        },
        "use bonds": {
            "default": "no",
            "kind": "boolean",
            "default_units": "",
            "enumeration": ("yes", "no"),
            "format_string": "s",
            "description": "Replace bonds in structure:",
            "help_text": "Replace the bonds on the structure.",
        },
        "adjust charge": {
            "default": "no",
            "kind": "boolean",
            "default_units": "",
            "enumeration": ("yes", "no"),
            "format_string": "s",
            "description": "Adjust charge on structure:",
            "help_text": "Adjust the charge on the structure.",
        },
        "ignore errors": {
            "default": "no",
            "kind": "boolean",
            "default_units": "",
            "enumeration": ("yes", "no"),
            "format_string": "s",
            "description": "Convert errors to warnings:",
            "help_text": "Only warn about errors, do not stop.",
        },
        "on errors use connectivity": {
            "default": "yes",
            "kind": "boolean",
            "default_units": "",
            "enumeration": ("yes", "no"),
            "format_string": "s",
            "description": "On errors, use connectivity instead:",
            "help_text": "Fallback to simple connectivity if Lewis structure fails.",
        },
        "results": {
            "default": {},
            "kind": "dictionary",
            "default_units": "",
            "enumeration": tuple(),
            "format_string": "",
            "description": "results",
            "help_text": "The results to save to variables or in tables.",
        },
    }

    def __init__(self, defaults={}, data=None):
        """Initialize the instance, by default from the default
        parameters given in the class"""

        super().__init__(
            defaults={**LewisStructureParameters.parameters, **defaults}, data=data
        )
