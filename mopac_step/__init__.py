# -*- coding: utf-8 -*-

"""Top-level package for MOPAC step."""

__author__ = """Paul Saxe"""
__email__ = 'psaxe@molssi.org'

# Handle versioneer
from ._version import get_versions  # noqa: E402
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions

# Bring up the classes so that they appear to be directly in
# the package.

from mopac_step.mopac_metadata import keywords, properties  # noqa: F401
from mopac_step.mopac_step import MOPACStep  # noqa: F401
from mopac_step.mopac import MOPAC  # noqa: F401
from mopac_step.tk_mopac import TkMOPAC  # noqa: F401
from mopac_step.energy_step import EnergyStep  # noqa: F401
from mopac_step.energy import Energy  # noqa: F401
from mopac_step.energy_parameters import EnergyParameters  # noqa: F401
from mopac_step.tk_energy import TkEnergy  # noqa: F401
from mopac_step.optimization_step import OptimizationStep  # noqa: F401
from mopac_step.optimization import Optimization  # noqa: F401
from mopac_step.optimization_parameters import OptimizationParameters  # noqa: F401 E501
from mopac_step.tk_optimization import TkOptimization  # noqa: F401
from mopac_step.ir_step import IRStep  # noqa: F401
from mopac_step.ir import IR  # noqa: F401
from mopac_step.ir_parameters import IRParameters  # noqa: F401
from mopac_step.tk_ir import TkIR  # noqa: F401
from mopac_step.thermodynamics_step import ThermodynamicsStep  # noqa: F401
from mopac_step.thermodynamics import Thermodynamics  # noqa: F401
from mopac_step.thermodynamics_parameters import ThermodynamicsParameters  # noqa: F401 E501
from mopac_step.tk_thermodynamics import TkThermodynamics  # noqa: F401
