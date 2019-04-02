# -*- coding: utf-8 -*-
"""Setup and run MOPAC"""

import json
import logging
import molssi_workflow
from molssi_workflow import ureg, Q_, units_class, data  # nopep8
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
        self._long_header = []
        self._long_header.append(__(self.header, indent=3*' '))

        P = self.parameters.current_values_to_dict(
            context=molssi_workflow.workflow_variables._data
        )
        # Have to fix formatting for printing...
        PP = dict(P)
        for key in PP:
            if isinstance(PP[key], units_class):
                PP[key] = '{:~P}'.format(PP[key])

        self._long_header.append(
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

        text = self._long_header

        # The results
        printer.normal(
            __(('\nThe SCF converged in {NUMBER_SCF_CYCLES} iterations '
                'to a heat of formation of {HEAT_OF_FORMATION} '
                'kcal/mol.'), **data, indent='   '
            )
        )

        # Print the amended properties structure, if desired
        # Used to update the properties data structure
        if False:
            properties = dict(mopac_step.properties)
            for key in data:
                if key not in properties:
                    print("key '{}' not in properties!?".format(key))
                else:
                    entry = properties[key]
                    if 'calculation' not in entry:
                        entry['calculation'] = ['single point energy']
                    else:
                        if 'single point energy' not in entry['calculation']:
                            entry['calculation'].append('single point energy')
            print('properties:\n')
            print(json.dumps(properties, indent=4, sort_keys=True))
            print()

        # Put any requested results into variables or tables
        results = self.parameters['results'].value
        for key, value in results.items():
            if 'variable' in value:
                self.set_variable(value['variable'], data[key])

            if 'table' in value:
                tablename = value['table']
                column = value['column']
                # Does the table exist?
                if not self.variable_exists(tablename):
                    if self.parameters['create tables'].get():
                        table = pandas.DataFrame()
                        self.set_variable(
                            tablename, {
                                'type': 'pandas',
                                'table': table,
                                'defaults': {},
                                'loop index': False,
                                'current index': 0
                            }
                        )
                    else:
                        raise RuntimeError(
                            "Table '{}' does not exist.".format(tablename)
                        )

                table_handle = self.get_variable(tablename)
                table = table_handle['table']

                # create the column as needed
                if column not in table.columns:
                    kind = mopac_step.properties[key]['type']
                    if kind == 'boolean':
                        default = False
                    elif kind == 'integer':
                        default = 0
                    elif kind == 'float':
                        default = np.nan
                    else:
                        default  = ''

                    table_handle['defaults'][column] = default
                    table[column] = default

                # and put the value in (finally!!!)
                row_index = table_handle['current index']
                table.at[row_index, column] = data[key]

        return text
