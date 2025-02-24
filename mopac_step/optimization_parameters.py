# -*- coding: utf-8 -*-
"""Control parameters for a MOPAC optimization calculation"""

import logging
import mopac_step

logger = logging.getLogger(__name__)


class OptimizationParameters(mopac_step.EnergyParameters):
    """The control parameters for optimization in MOPAC"""

    parameters = {
        "method": {
            "default": "default",
            "kind": "enumeration",
            "default_units": "",
            "enumeration": (
                "default",
                "EF -- eigenvector following",
                "BFGS -- Broyden-Fletcher-Goldfarb-Shanno algorithm",
                "L-BFGS -- smaller memory BFGS for larger systems",
                "TS -- transition state with EF method",
                "SIGMA -- transition state with McIver-Komornicki method",
                "NLLSQ -- nonlinear least squares of gradient, Bartel's method",
            ),
            "format_string": "s",
            "description": "Optimization algorithm:",
            "help_text": ("The optimization algorithm to use."),
        },
        "gnorm": {
            "default": "1.0",
            "kind": "float",
            "default_units": "kcal/mol/Å",
            "enumeration": tuple(),
            "format_string": ".1f",
            "description": "Convergence criterion:",
            "help_text": (
                "The convergence criterion for the optimization. "
                "This is controlled in part by the overall "
                "convergence criterion:"
                "* 'normal' is the default level, 1.0 "
                " kcal/mol/Å."
                "* 'precise' tightens up the criterion by a factor "
                "of 100."
                "* 'absolute' uses the value set here."
            ),
        },
        "cycles": {
            "default": "unlimited",
            "kind": "integer",
            "default_units": "",
            "enumeration": ("unlimited",),
            "format_string": "",
            "description": "Maximum steps:",
            "help_text": (
                "The maximum number of steps to take "
                "in the optimization. 'unlimited' means "
                "there is no definite limit; however, the "
                "time-limit of the job will stop the job."
            ),
        },
        "recalc": {
            "default": "never",
            "kind": "integer",
            "default_units": "",
            "enumeration": ("never",),
            "format_string": "",
            "description": "Recalculate Hessian:",
            "help_text": (
                "How often to recalculate the Hessian "
                "(in steps) "
                "when using the EF method. Smaller values "
                "help convergence but are expensive. 10 "
                "with a trust radius of 0.1 is useful for "
                "difficult cases, while 1 and a trust radius "
                "of 0.05 will always find a stationary point "
                "if one exists."
            ),
        },
        "dmax": {
            "default": "0.2",
            "kind": "float",
            "default_units": "",
            "enumeration": tuple(),
            "format_string": ".1f",
            "description": "Trust radius:",
            "help_text": (
                "The trust radius in the EF method. The "
                "algorithm updates this based on progress. "
                "The default is normally fine, but in some "
                "difficult cases reducing to 0.1 or 0.05 "
                "may be useful."
            ),
        },
        "LatticeOpt": {
            "default": "Yes",
            "kind": "boolean",
            "default_units": "",
            "enumeration": ("Yes", "No"),
            "format_string": "",
            "description": "Optimize the cell (if periodic):",
            "help_text": "Allow the lattice vectors to change during optimization.",
        },
        "pressure": {
            "default": 0.0,
            "kind": "float",
            "default_units": "GPa",
            "enumeration": tuple(),
            "format_string": ".1f",
            "description": "Pressure:",
            "help_text": ("The applied pressure."),
        },
    }

    def __init__(self, defaults={}, data=None):
        """Initialize the instance, by default from the default
        parameters given in the class"""

        super().__init__(
            defaults={
                **OptimizationParameters.parameters,
                **defaults,
            },
            data=data,
        )

        # Do any local editing of defaults
        tmp = self["structure handling"]
        tmp.description = "Structure handling:"

        tmp = self["system name"]
        tmp._data["enumeration"] = (*tmp.enumeration, "optimized with {Hamiltonian}")
        tmp.default = "keep current name"

        tmp = self["configuration name"]
        tmp._data["enumeration"] = ["optimized with {Hamiltonian}", *tmp.enumeration]
        tmp.default = "optimized with {Hamiltonian}"
