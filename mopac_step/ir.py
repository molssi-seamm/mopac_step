# -*- coding: utf-8 -*-

"""Run a vibrational frequency calculation in MOPAC"""

import logging
import seamm
import seamm_util.printing as printing
from seamm_util.printing import FormattedText as __
import mopac_step

logger = logging.getLogger(__name__)
job = printing.getPrinter()
printer = printing.getPrinter('mopac')


class IR(mopac_step.Energy):

    def __init__(self, flowchart=None, title='IR Spectrum', extension=None):
        """Initialize the node"""

        logger.debug('Creating IR {}'.format(self))

        super().__init__(flowchart=flowchart, title=title, extension=extension)

        self.parameters = mopac_step.IRParameters()
        self.description = 'Infrared (vibrational) spectroscopy calculation'

    def description_text(self, P=None):
        """Prepare information about what this node will do
        """

        if not P:
            P = self.parameters.values_to_dict()

        text = (
            'Harmonic vibrational calculation using {hamiltonian}, '
            'with the SCF converged to '
        )
        # Convergence
        if P['convergence'] == 'normal':
            text += "the 'normal' level of 1.0e-07 kcal/mol."
        elif P['convergence'] == 'precise':
            text += "the 'precise' level of 1.0e-09 kcal/mol."
        elif P['convergence'] == 'relative':
            text += ('a factor of {relative} times the ' 'normal criterion.')
        elif P['convergence'] == 'absolute':
            text += 'converged to {absolute}.'

        if P['trans'] != 0:
            text += (
                '\n\nA total of {trans} lowest modes will be ignored to '
                'approximately account for {trans} internal rotations.'
            )

        return self.header + '\n' + __(text, **P, indent=4 * ' ').__str__()

    def get_input(self):
        """Get the input for an optimization MOPAC"""

        P = self.parameters.current_values_to_dict(
            context=seamm.flowchart_variables._data
        )

        # Remove the 1SCF keyword from the energy setup
        keywords = []
        for keyword in super().get_input():
            if keyword == '1SCF':
                keywords.append('FORCE')
                if P['trans'] != 0:
                    keywords.append('TRANS={}'.format(P['trans']))
                if P['let']:
                    keywords.append('LET')
            else:
                keywords.append(keyword)

        return keywords

    def analyze(self, indent='', data={}, out=[]):
        """Parse the output and generating the text output and store the
        data in variables for other stages to access
        """

        printer.normal(self._long_header)

        # The results
        printer.normal(
            __(
                (
                    '\nThe geometry converged in {NUMBER_SCF_CYCLES} '
                    'iterations to a heat of formation of {HEAT_OF_FORMATION} '
                    'kcal/mol.'
                ),
                **data,
                indent=7 * ' '
            )
        )

        # Put any requested results into variables or tables
        self.store_results(
            data=data,
            properties=mopac_step.properties,
            results=self.parameters['results'].value,
            create_tables=self.parameters['create tables'].get()
        )

        printer.normal('\n')
