# -*- coding: utf-8 -*-

"""Setup and run MOPAC"""

import logging
import seamm
import seamm_util.printing as printing
from seamm_util.printing import FormattedText as __
import mopac_step

logger = logging.getLogger(__name__)
job = printing.getPrinter()
printer = printing.getPrinter('mopac')


class Optimization(mopac_step.Energy):

    def __init__(self, flowchart=None, title='Optimization', extension=None):
        """Initialize the node"""

        logger.debug('Creating Optimization {}'.format(self))

        super().__init__(flowchart=flowchart, title=title, extension=extension)

        self.parameters = mopac_step.OptimizationParameters()

        self.description = 'A structural optimization'

    def description_text(self, P=None):
        """Prepare information about what this node will do
        """

        if not P:
            P = self.parameters.values_to_dict()

        # Hamiltonian followed by convergence
        text = 'Geometry optimization using {hamiltonian}'
        if P['method'] == 'default':
            text += (
                ' and default optimizer (EF for small systems,'
                ' L-BFGS for larger).'
            )
        elif P['method'][0:1] == 'EF':
            text += ' and the eigenvector following (EF) method.'
        elif P['method'][0:3] == 'BFGS':
            text += ' and the BFGS method.'
        elif P['method'][0:5] == 'L-BFGS':
            text += ' and the L-BFGS small memory version of the BFGS method.'
        else:
            text += (
                ". The optimization method will be determined at runtime "
                "by '{method}'."
            )

        if P['gnorm'] == 'default':
            text += (
                ' The geometrical convergence is the default of '
                '1.0 kcal/mol/Å.'
            )
        elif P['gnorm'][0] == '$':
            text += (
                ' The geometrical convergence will be determined '
                "at runtime by '{gnorm}'."
            )
        else:
            text += ' The geometrical convergence is {gnorm} kcal/mol/Å.'

        # SCF convergence
        text += ' The SCF will be converged to '
        if P['convergence'] == 'normal':
            text += 'the normal level of 1.0e-04 kcal/mol'
        elif P['convergence'] == 'precise':
            text += "the 'precise' level of 1.0e-06 kcal/mol"
        elif P['convergence'] == 'relative':
            text += 'a factor of {relative} times the normal criteria'
        elif P['convergence'] == 'absolute':
            text += ' {absolute} kcal/mol'

        return self.header + '\n' + __(text, **P, indent=4 * ' ').__str__()

    def get_input(self):
        """Get the input for an optimization MOPAC"""

        P = self.parameters.current_values_to_dict(
            context=seamm.flowchart_variables._data
        )

        # Remove the 1SCF keyword from the energy setup
        keywords = []
        for keyword in super().get_input():
            if keyword != '1SCF':
                keywords.append(keyword)

        # and the optimization-specific parts
        method = P['method']
        if method == 'default':
            pass
        elif method[0:2] == 'EF':
            keywords.append('EF')
            if P['recalc'] != 'never':
                keywords.append(P['recalc'])
            if P['dmax'] != self.parameters['dmax'].default:
                keywords.append(P['dmax'])
            elif method[0:4] == 'BFGS':
                keywords.append('BFGS')
            elif method[0:6] == 'L-BFGS':
                keywords.append('L-BFGS')
            elif method[0:2] == 'TS':
                keywords.append('TS')
            elif method[0:5] == 'SIGMA':
                keywords.append('SIGMA')
            elif method[0:5] == 'NLLSQ':
                keywords.append('NLLSQ')
            else:
                text = (
                    "Don't recognize optimization method '{}'".format(
                        P['method']
                    )
                )
                logger.critical(text)
                raise RuntimeError(text)

        if P['cycles'] != 'unlimited':
            keywords.append('CYCLES={}'.format(P['cycles']))
        if P['convergence'] == 'absolute':
            if P['gnorm'] != self.parameters['gnorm'].default:
                keywords.append('GNORM={}'.format(P['gnorm']))

        return keywords

    def analyze(self, indent='', data={}):
        """Parse the output and generating the text output and store the
        data in variables for other stages to access
        """

        printer.normal(self._long_header)

        # The results
        if 'NUMBER_SCF_CYCLES' in data:
            printer.normal(
                __(
                    (
                        '\nThe geometry optimization converged in '
                        '{NUMBER_SCF_CYCLES} iterations to a heat of '
                        'formation of {HEAT_OF_FORMATION} kcal/mol and '
                        'gradient norm of {GRADIENT_NORM} kcal/mol/Å.'
                    ),
                    **data,
                    indent=7 * ' '
                )
            )
        else:
            data['NUMBER_SCF_CYCLES'] = len(data['HEAT_OF_FORM_UPDATED'])
            data['HEAT_OF_FORMATION'] = data['HEAT_OF_FORM_UPDATED'][-1]
            data['GRADIENT_NORM'] = data['GRADIENT_UPDATED'][-1]
            printer.normal(
                __(
                    (
                        '\nThe geometry optimization did not converge!\n'
                        'It ran for {NUMBER_SCF_CYCLES} '
                        'iterations to a final heat of formation of '
                        '{HEAT_OF_FORMATION} kcal/mol and gradient norm '
                        'of {GRADIENT_NORM} kcal/mol/Å.'
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
