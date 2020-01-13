# -*- coding: utf-8 -*-

"""Run a thermodynamics calculation in MOPAC"""

import logging
import seamm
import seamm_util.printing as printing
from seamm_util.printing import FormattedText as __
import mopac_step

logger = logging.getLogger(__name__)
job = printing.getPrinter()
printer = printing.getPrinter('mopac')


class Thermodynamics(mopac_step.Energy):

    def __init__(self, flowchart=None, title='Thermodynamics', extension=None):
        """Initialize the node"""

        logger.debug('Creating Thermodynamics {}'.format(self))

        super().__init__(flowchart=flowchart, title=title, extension=extension)

        self.parameters = mopac_step.ThermodynamicsParameters()

        self.description = 'Thermodynamic functions'

    def description_text(self, P=None):
        """Prepare information about what this node will do
        """

        if not P:
            P = self.parameters.values_to_dict()

        text = 'Thermodynamics calculation using {hamiltonian}, converged to '
        # Convergence
        if P['convergence'] == 'normal':
            text += "the 'normal' level of 1.0e-04 kcal/mol."
        elif P['convergence'] == 'precise':
            text += "the 'precise' level of 1.0e-06 kcal/mol."
        elif P['convergence'] == 'relative':
            text += ('a factor of {relative} times the ' 'normal criterion.')
        elif P['convergence'] == 'absolute':
            text += 'converged to {absolute}.'

        text += (
            '\nThe thermodynamics functions will be calculated from '
            '{Tmin} to {Tmax} in steps of {Tstep}. {trans} lowest '
            'modes will be ignored to approximately account for {trans} '
            'internal rotations.'
        )

        return self.header + '\n' + __(text, **P, indent=4 * ' ').__str__()

    def get_input(self):
        """Get the input for thermodynamics in MOPAC"""

        P = self.parameters.current_values_to_dict(
            context=seamm.flowchart_variables._data
        )

        # Convert values with unts to the right units, and remove
        # the unit string.
        for key in ('Tmax', 'Tmin', 'Tstep'):
            P[key] = P[key].to('K').magnitude

        # Remove the 1SCF keyword from the energy setup
        keywords = []
        for keyword in super().get_input():
            if keyword == '1SCF':
                keywords.append('THERMO=({Tmin},{Tmax},{Tstep})'.format(**P))
                keywords.append('TRANS={trans}'.format(**P))
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
