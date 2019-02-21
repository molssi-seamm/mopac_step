# -*- coding: utf-8 -*-
"""Setup and run MOPAC"""

import logging
import molssi_workflow
import mopac_step

logger = logging.getLogger(__name__)


methods = (
    'default',
    'EF -- eigenvector following',
    'BFGS -- Broyden-Fletcher-Goldfarb-Shanno algorithm',
    'L-BFGS -- smaller memory BFGS for larger systems',
    'TS -- transition state with EF method',
    'SIGMA -- transition state with McIver-Komornicki method',
    "NLLSQ -- nonlinear least squares of gradient, Bartel's method",
    )


class Optimization(mopac_step.Energy):
    def __init__(self, workflow=None, title='Optimization', extension=None):
        """Initialize the node"""

        logger.debug('Creating Optimization {}'.format(self))

        self.method = 'default'  # The optimization method to use
        self.cycles = None  # Maximum number of geometry steps
        self.recalc = None  # How often to recalculate the hessian in EF method
        self.dmax = None  # initial trust radius in EF method, default 0.2
        self.gnorm = None  # gradient norm for convergence, dflt 1.0 kcal/mol/Å
   
        super().__init__(workflow=workflow, title=title, extension=extension)

        self.description = 'A structural optimization'

    def describe(self, indent='', json_dict=None):
        """Write out information about what this node will do
        If json_dict is passed in, add information to that dictionary
        so that it can be written out by the controller as appropriate.
        """

        next_node = molssi_workflow.Node.describe(self, indent, json_dict)
                    
        # Hamiltonian followed by convergence
        if self.method == 'default':
            tmp = ' and default optimizer (EF for small systems,' + \
                  ' L-BFGS for larger)'
        elif self.method[0:1] == 'EF':
            tmp = ' and the eigenvector following (EF) method'
        elif self.method[0:3] == 'BFGS':
            tmp = ' and the BFGS method'
        elif self.method[0:5] == 'L-BFGS':
            tmp = ' and the L-BFGS small memory version of the BFGS method'
        else:
            raise RuntimeError("Don't understand optimizer '{}'".format(
                self.method)
            )

        self.job_output(indent + '   Geometry optimization using ' +
                        self.hamiltonian + tmp)

        if self.gnorm is None:
            self.job_output(indent + '   The geometrical convergence is ' +
                            'the default of 1.0 kcal/mol/Å'
                            )
        else:
            self.job_output(indent + '   The geometrical convergence is ' +
                            '{} kcal/mol/Å'.format(self.gnorm)
                            )
            
        # SCF convergence
        if self.convergence == 'default':
            tmp = 'the normal level of 1.0e-04 kcal/mol'
        elif self.convergence == 'precise':
            tmp = "the 'precise' level of 1.0e-06 kcal/mol"
        elif self.convergence == 'relative':
            tmp = 'a factor of {}'.format(self.relscf) \
                  + ' times the normal criteria'
        elif self.convergence == 'absolute':
            tmp = ' {} kcal/mol'.format(self.scfcrt)
        self.job_output(indent + '    The SCF will be converged to ' + tmp)
        slef.job_output('')

        return next_node

    def get_input(self):
        """Get the input for an optimization MOPAC"""

        # Remove the 1SCF keyword from the energy setup
        keywords = []
        for keyword in super().get_input():
            if keyword != '1SCF':
                keywords.append(keyword)

        return keywords
