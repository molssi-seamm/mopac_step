# -*- coding: utf-8 -*-
"""Setup and run MOPAC"""

import molssi_workflow
import logging

logger = logging.getLogger(__name__)


class Energy(molssi_workflow.Node):
    structures = {
        'current': '',
        'initial': '',
        'other': '',
    }

    hamiltonians = {
        'AM1': '',
        'MNDO': '',
        'MNDOD': '',
        'PM3': '',
        'PM6': '',
        'PM6-D3': '',
        'PM6-DH+': '',
        'PM6-DH2': '',
        'PM6-DH2X': '',
        'PM6-D3H4': '',
        'PM6-D3H4X': '',
        'PM7': '',
        'PM7-TS': '',
        'RM1': '',
    }

    convergences = {
        'default': '',
        'precise': '',
        'relative': '',
        'absolute': '',
    }

    def __init__(self, workflow=None, title='Energy', extension=None):
        """Initialize the node"""

        logger.debug('Creating Energy {}'.format(self))

        super().__init__(workflow=workflow, title=title, extension=extension)

        self.description = 'A single point energy calculation'

        self.structure = None
        self.hamiltonian = 'PM7'
        self.convergence = 'default'  # 'precise', 'relative' or 'absolute'
        self.relscf = 1.0  # SCF relative convergence, > 1 is less accurate
        self.scfcrt = 0.0001  # kcal/mol, SCF convergence
        self.keywords = []  # additional keywords to add

    def describe(self, indent='', json_dict=None):
        """Write out information about what this node will do
        If json_dict is passed in, add information to that dictionary
        so that it can be written out by the controller as appropriate.
        """

        next_node = super().describe(indent, json_dict)

        # Convergence
        if self.convergence == 'default':
            tmp = ' converged to the normal level of 1.0e-04 kcal/mol'
        elif self.convergence == 'precise':
            tmp = " converged to the 'precise' level of 1.0e-06 kcal/mol"
        elif self.convergence == 'relative':
            tmp = '\n' + indent + '    converged to a factor of' \
                  + ' {}'.format(self.relscf) \
                  + ' times the normal criteria'
        elif self.convergence == 'absolute':
            tmp = ' converged to {} kcal/mol'.format(self.scfcrt)
                    
        # Hamiltonian followed by converegence
        self.job_output(indent +
                        '   Single-point energy using ' +
                        self.hamiltonian + tmp
                        )
        self.job_output('')

        return next_node

    def get_input(self):
        """Get the input for an energy calculation for MOPAC"""

        keywords = [self.hamiltonian]

        keywords.append('1SCF')

        # which structure? may need to set default first...
        if not self.structure:
            if isinstance(self.previous(), molssi_workflow.StartNode):
                self.structure = 'initial'
            else:
                self.structure = 'current'

        if self.structure == 'current':
            keywords.append('OLDGEO')

        if self.convergence == 'default':
            pass
        elif self.convergence == 'precise':
            keywords.append('PRECISE')
        elif self.convergence == 'relative':
            keywords.append('RELSCF=' + self.relscf)
        elif self.convergence == 'absolute':
            keywords.append('SCFSCRT=' + self.scfcrt)
        else:
            raise RuntimeError("Don't recognize convergence '{}'".format(
                self.convergence))

        return keywords

    def analyze(self, indent='', data={}):
        """Parse the output and generating the text output and store the
        data in variables for other stages to access
        """
        result = ''

        result += 'Step ' + '.'.join(str(e) for e in self._id)
        result += ': ' + self.title

        # Convergence
        if self.convergence == 'default':
            tmp = ' converged to the normal level of 1.0e-04 kcal/mol'
        elif self.convergence == 'precise':
            tmp = " converged to the 'precise' level of 1.0e-06 kcal/mol"
        elif self.convergence == 'relative':
            value = molssi_workflow.workflow_variables.value(self.relscf)
            tmp = '\n  converged to a factor of' \
                  + ' {}'.format(self.value) \
                  + ' times the normal criteria' \
                  + ' = {} kcal/mol'.format(1.0e-04*value)
        elif self.convergence == 'absolute':
            value = molssi_workflow.workflow_variables.value(self.scfcrt)
            tmp = ' converged to {} kcal/mol'.format(self.scfcrt)
                    
        # Hamiltonian followed by converegence
        result += '\n  Single-point energy using '
        result += self.hamiltonian + tmp

        # The results
        result += '\n'
        result += "\n  The SCF converged in {} iterations".format(
            data['NUMBER_SCF_CYCLES']
        )
        result += " to a heat of formation of {} kcal/mol".format(
            data['HEAT_OF_FORMATION']
        )
        result += '\n'

        # And set the global variables to store key results
        molssi_workflow.workflow_variables['calculated heat of formation'] \
            = data['HEAT_OF_FORMATION']

        return result
