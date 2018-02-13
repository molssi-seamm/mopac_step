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
        elif self.convergence == 'manual':
            keywords.append('SCFSCRT=' + self.scfcrt)
        else:
            raise RuntimeError("Don't recognize convergence '{}'".format(
                self.convergence))

        return keywords
