# -*- coding: utf-8 -*-

"""Top-level package for MOPAC step."""

# Bring up the classes so that they appear to be directly in
# the package.

from .mopac_base import MOPACBase  # noqa: F401

from .lewis_structure_step import LewisStructureStep  # noqa: F401
from .lewis_structure import LewisStructure  # noqa: F401
from .lewis_structure_parameters import LewisStructureParameters  # noqa: F401
from .tk_lewis_structure import TkLewisStructure  # noqa: F401

from .mopac_step import MOPACStep  # noqa: F401
from .mopac import MOPAC  # noqa: F401
from .tk_mopac import TkMOPAC  # noqa: F401
from .energy_step import EnergyStep  # noqa: F401
from .energy import Energy  # noqa: F401
from .energy_parameters import EnergyParameters  # noqa: F401
from .tk_energy import TkEnergy  # noqa: F401
from .forceconstants_step import ForceconstantsStep  # noqa: F401
from .forceconstants import Forceconstants  # noqa: F401
from .forceconstants_parameters import ForceconstantsParameters  # noqa: F401
from .tk_forceconstants import TkForceconstants  # noqa: F401
from .optimization_step import OptimizationStep  # noqa: F401
from .optimization import Optimization  # noqa: F401
from .optimization_parameters import OptimizationParameters  # noqa: F401
from .tk_optimization import TkOptimization  # noqa: F401
from .ir_step import IRStep  # noqa: F401
from .ir import IR  # noqa: F401
from .ir_parameters import IRParameters  # noqa: F401
from .tk_ir import TkIR  # noqa: F401
from .thermodynamics_step import ThermodynamicsStep  # noqa: F401
from .thermodynamics import Thermodynamics  # noqa: F401
from .thermodynamics_parameters import (  # noqa: F401
    ThermodynamicsParameters,
)
from .tk_thermodynamics import TkThermodynamics  # noqa: F401

from .metadata import metadata  # noqa: F401

# Handle versioneer
from ._version import get_versions

__author__ = """Paul Saxe"""
__email__ = "psaxe@molssi.org"
versions = get_versions()
__version__ = versions["version"]
__git_revision__ = versions["full-revisionid"]
del get_versions, versions
