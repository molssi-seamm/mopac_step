# -*- coding: utf-8 -*-
"""Control parameters for a MOPAC single-point energy calculation
"""

import logging
import seamm

logger = logging.getLogger(__name__)


class EnergyParameters(seamm.Parameters):
    """The control parameters for creating a structure from SMILES"""

    parameters = {
        "structure": {
            "default": "default",
            "kind": "enumeration",
            "default_units": "",
            "enumeration": (
                'default',
                'initial',
                'current',
            ),
            "format_string": "s",
            "description": "Structure:",
            "help_text": ("The structure to use. By default, for the "
                          "first calculation the incoming structure is "
                          "used, and subsequently that from the previous "
                          "MOPAC steps.")
        },
        "hamiltonian": {
            "default": "PM7",
            "kind": "enumeration",
            "default_units": "",
            "enumeration": (
                'AM1',
                'MNDO',
                'MNDOD',
                'PM3',
                'PM6',
                'PM6-D3',
                'PM6-DH+',
                'PM6-DH2',
                'PM6-DH2X',
                'PM6-D3H4',
                'PM6-D3H4X',
                'PM7',
                'PM7-TS',
                'RM1',
            ),
            "format_string": "s",
            "description": "Hamiltonian:",
            "help_text": ("The Hamiltonian (parameterization) to use.")
        },
        "convergence": {
            "default": "normal",
            "kind": "enumeration",
            "default_units": "",
            "enumeration": (
                'normal',
                'precise',
                'relative',
                'absolute',
            ),
            "format_string": "s",
            "description": "Convergence criterion:",
            "help_text": ("The convergence criterion for the energy. "
                          "* 'normal' is the default level, 1.0E-04 "
                          " kcal/mol for SCF. For force contants, transition "
                          " state searches, etc. the default is 1.0E-07."
                          "* 'precise' tightens up the criterion by a factor "
                          "of 100."
                          "* 'relative' multiplies the SCF convergence "
                          "criterion by the amount given. Values >1 loosen "
                          "the tolerance, while values <1 tighten it."
                          "* 'absolute' sets the criterion directly.")
        },
        "relative": {
            "default": "0.1",
            "kind": "float",
            "default_units": "",
            "enumeration": tuple(),
            "format_string": "",
            "description": "factor",
            "help_text": ("The factor to multiply the default SCF "
                          "convergence criterion. Values >1 make the "
                          "criterion looser; < 1, tighter.")
        },
        "absolute": {
            "default": "1.0E-07",
            "kind": "float",
            "default_units": "kcal/mol",
            "enumeration": tuple(),
            "format_string": "",
            "description": "criterion",
            "help_text": ("The SCF convergence criterion, based on the "
                          "change in energy between iterations.")
        },
        "extra keywords": {
            "default": [],
            "kind": "list",
            "default_units": "",
            "enumeration": tuple(),
            "format_string": "",
            "description": "Extra keywords",
            "help_text": ("Extra keywords to append to those from the GUI. "
                          "This allows you to add to and override the GUI.")
        },
        "results": {
            "default": {},
            "kind": "dictionary",
            "default_units": "",
            "enumeration": tuple(),
            "format_string": "",
            "description": "results",
            "help_text": ("The results to save to variables or in "
                          "tables. ")
        },
        "create tables": {
            "default": "yes",
            "kind": "boolean",
            "default_units": "",
            "enumeration": ('yes', 'no'),
            "format_string": "",
            "description": "Create tables as needed:",
            "help_text": ("Whether to create tables as needed for "
                          "results being saved into tables.")
        },
    }

    def __init__(self, defaults={}, data=None):
        """Initialize the instance, by default from the default
        parameters given in the class"""

        super().__init__(
            defaults={**EnergyParameters.parameters, **defaults},
            data=data
        )
