# -*- coding: utf-8 -*-
"""Setup and run MOPAC"""

import json
import logging
import molssi_workflow
from molssi_workflow import units_class  # nopep8
import molssi_util.printing as printing
from molssi_util.printing import FormattedText as __
import mopac_step
import numpy as np
import pandas

logger = logging.getLogger(__name__)
job = printing.getPrinter()
printer = printing.getPrinter('mopac')


class Energy(molssi_workflow.Node):

    def __init__(self, workflow=None, title='Energy', extension=None):
        """Initialize the node"""

        logger.debug('Creating Energy {}'.format(self))

        super().__init__(workflow=workflow, title=title, extension=extension)

        self.parameters = mopac_step.EnergyParameters()

        self.description = 'A single point energy calculation'
        self._long_header = ''
        self.keywords = []  # additional keywords to add

    def description_text(self, P):
        """Prepare information about what this node will do
        """

        text = 'Single-point energy using {hamiltonian}, converged to '
        # Convergence
        if P['convergence'] == 'normal':
            text += "the 'normal' level of 1.0e-04 kcal/mol."
        elif P['convergence'] == 'precise':
            text += "the 'precise' level of 1.0e-06 kcal/mol."
        elif P['convergence'] == 'relative':
            text += ('a factor of {relative} times the '
                     'normal criterion.')
        elif P['convergence'] == 'absolute':
            text += 'converged to {absolute}'

        return text

    def get_input(self):
        """Get the input for an energy calculation for MOPAC"""
        self._long_header = ''
        self._long_header += str(__(self.header, indent=3*' '))
        self._long_header += '\n'

        P = self.parameters.current_values_to_dict(
            context=molssi_workflow.workflow_variables._data
        )
        # Have to fix formatting for printing...
        PP = dict(P)
        for key in PP:
            if isinstance(PP[key], units_class):
                PP[key] = '{:~P}'.format(PP[key])

        self._long_header += str(
            __(self.description_text(PP), **PP, indent=7*' ')
        )

        # Start gathering the keywords
        keywords = ['1SCF', P['hamiltonian']]

        # which structure? may need to set default first...
        if P['structure'] == 'default':
            if self._id[-1] == '1':
                structure = 'initial'
            else:
                structure = 'current'
        elif self._id[-1] == '1':
            structure = 'initial'
        elif P['structure'] == 'current':
            structure = 'current'

        if structure == 'current':
            keywords.append('OLDGEO')

        if P['convergence'] == 'normal':
            pass
        elif P['convergence'] == 'precise':
            keywords.append('PRECISE')
        elif P['convergence'] == 'relative':
            keywords.append('RELSCF=' + P['relative'])
        elif P['convergence'] == 'absolute':
            keywords.append('SCFSCRT=' + P['absolute'])
        else:
            raise RuntimeError("Don't recognize convergence '{}'".format(
                P['convergence']))

        return keywords

    def analyze(self, indent='', data={}):
        """Parse the output and generating the text output and store the
        data in variables for other stages to access
        """

        printer.normal(self._long_header)

        # Put any requested results into variables or tables
        self.store_results(
            data=data,
            properties=mopac_step.properties,
            results=self.parameters['results'].value,
            create_tables=self.parameters['create tables'].get()
        )

        printer.normal('\n')
