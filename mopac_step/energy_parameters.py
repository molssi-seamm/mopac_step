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
                "default",
                "initial",
                "current",
            ),
            "format_string": "s",
            "description": "Structure:",
            "help_text": (
                "The structure to use. By default, for the "
                "first calculation the incoming structure is "
                "used, and subsequently that from the previous "
                "MOPAC steps."
            ),
        },
        "hamiltonian": {
            "default": "PM7",
            "kind": "enumeration",
            "default_units": "",
            "enumeration": (
                "AM1",
                "MNDO",
                "MNDOD",
                "PM3",
                "PM6",
                "PM6-D3",
                "PM6-DH+",
                "PM6-DH2",
                "PM6-DH2X",
                "PM6-D3H4",
                "PM6-D3H4X",
                "PM7",
                "PM7-TS",
                "RM1",
            ),
            "format_string": "s",
            "description": "Hamiltonian:",
            "help_text": ("The Hamiltonian (parameterization) to use."),
        },
        "convergence": {
            "default": "normal",
            "kind": "enumeration",
            "default_units": "",
            "enumeration": (
                "normal",
                "precise",
                "relative",
                "absolute",
            ),
            "format_string": "s",
            "description": "Convergence criterion:",
            "help_text": (
                "The convergence criterion for the energy. "
                "* 'normal' is the default level, 1.0E-04 "
                " kcal/mol for SCF. For force contants, transition "
                " state searches, etc. the default is 1.0E-07."
                "* 'precise' tightens up the criterion by a factor "
                "of 100."
                "* 'relative' multiplies the SCF convergence "
                "criterion by the amount given. Values >1 loosen "
                "the tolerance, while values <1 tighten it."
                "* 'absolute' sets the criterion directly."
            ),
        },
        "uhf": {
            "default": "no",
            "kind": "boolean",
            "default_units": "",
            "enumeration": (
                "yes",
                "no",
            ),
            "format_string": "s",
            "description": "UHF for singlets:",
            "help_text": "Whether to use UHF for singlet states.",
        },
        "COSMO": {
            "default": "no",
            "kind": "boolean",
            "default_units": "",
            "enumeration": (
                "yes",
                "no",
            ),
            "format_string": "s",
            "description": "Solvent using COSMO:",
            "help_text": "Whether to use COSMO solvation model.",
        },
        "MOZYME": {
            "default": "for larger systems",
            "kind": "enumeration",
            "default_units": "",
            "enumeration": (
                "for larger systems",
                "always",
                "never",
            ),
            "format_string": "s",
            "description": "Use localized molecular orbitals (MOZYME):",
            "help_text": (
                "Whether and when to use localized molecular orbitals (LMO) by using "
                "MOZYME."
            ),
        },
        "nMOZYME": {
            "default": 300,
            "kind": "integer",
            "default_units": "",
            "enumeration": tuple(),
            "format_string": "",
            "description": "with this many atoms or more:",
            "help_text": ("The number of atoms to switch to using MOZYME."),
        },
        "MOZYME follow-up": {
            "default": (
                "recalculate the energy at the end using new, orthogonal localized "
                "orbitals"
            ),
            "kind": "enumeration",
            "default_units": "",
            "enumeration": (
                "recalculate the energy at the end using new, orthogonal localized "
                "orbitals",
                "recalculate the energy at the end using exact, non-localized orbitals",
                "none",
            ),
            "format_string": "s",
            "description": "Follow-up calculation:",
            "help_text": (
                "Whether to follow the localize molecular orbital calculation "
                "with another calculation to clean up the orbitals, or check "
                "by doing a full calculation without localizing the orbitals."
            ),
        },
        "eps": {
            "default": "78.4",
            "kind": "float",
            "default_units": "",
            "enumeration": tuple(),
            "format_string": "",
            "description": "Dielectric constant:",
            "help_text": "The solvent's dielectric constant.",
        },
        "rsolve": {
            "default": "1.3",
            "kind": "float",
            "default_units": "Å",
            "enumeration": tuple(),
            "format_string": "",
            "description": "Solvent radius:",
            "help_text": "The solvent's approximate radius.",
        },
        "nspa": {
            "default": 42,
            "kind": "integer",
            "default_units": "",
            "enumeration": (
                "12",
                "32",
                "42",
                "92",
                "122",
                "162",
                "252",
                "272",
                "362",
                "482",
                "492",
                "752",
                "812",
                "1082",
                "1442",
                "1472",
            ),
            "format_string": "",
            "description": "Surface grid size:",
            "help_text": (
                "The number of points in the solvent-accessible surface grid per atom."
            ),
        },
        "disex": {
            "default": "2.0",
            "kind": "float",
            "default_units": "",
            "enumeration": tuple(),
            "format_string": "",
            "description": "Cutoff:",
            "help_text": (
                "The cutoff for exact calculation of segment-segment interactions in "
                "COSMO."
            ),
        },
        "calculate gradients": {
            "default": "yes",
            "kind": "boolean",
            "default_units": "",
            "enumeration": (
                "yes",
                "no",
            ),
            "format_string": "s",
            "description": "Calculate gradients:",
            "help_text": "Whether to calculate the gradients.",
        },
        "relative": {
            "default": "0.1",
            "kind": "float",
            "default_units": "",
            "enumeration": tuple(),
            "format_string": "",
            "description": "factor",
            "help_text": (
                "The factor to multiply the default SCF "
                "convergence criterion. Values >1 make the "
                "criterion looser; < 1, tighter."
            ),
        },
        "absolute": {
            "default": "1.0E-07",
            "kind": "float",
            "default_units": "kcal/mol",
            "enumeration": tuple(),
            "format_string": "",
            "description": "criterion",
            "help_text": (
                "The SCF convergence criterion, based on the "
                "change in energy between iterations."
            ),
        },
        "bond orders": {
            "default": "yes",
            "kind": "enum",
            "default_units": "",
            "enumeration": ("yes", "yes, and apply to structure", "no"),
            "format_string": "",
            "description": "Calculate bond orders:",
            "help_text": "Whether to calculate bond orders and also apply to structure",
        },
        "extra keywords": {
            "default": [],
            "kind": "list",
            "default_units": "",
            "enumeration": tuple(),
            "format_string": "",
            "description": "Extra keywords",
            "help_text": (
                "Extra keywords to append to those from the GUI. "
                "This allows you to add to and override the GUI."
            ),
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
        "create tables": {
            "default": "yes",
            "kind": "boolean",
            "default_units": "",
            "enumeration": ("yes", "no"),
            "format_string": "",
            "description": "Create tables as needed:",
            "help_text": (
                "Whether to create tables as needed for "
                "results being saved into tables."
            ),
        },
    }

    def __init__(self, defaults={}, data=None):
        """Initialize the instance, by default from the default
        parameters given in the class"""

        super().__init__(
            defaults={**EnergyParameters.parameters, **defaults}, data=data
        )
