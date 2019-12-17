# -*- coding: utf-8 -*-

"""Setup and run MOPAC"""

import logging
import seamm
from seamm_util import ureg, Q_, units_class  # noqa: F401
import seamm_util.printing as printing
from seamm_util.printing import FormattedText as __
import mopac_step
import copy

logger = logging.getLogger(__name__)
job = printing.getPrinter()
printer = printing.getPrinter('mopac')


class Energy(seamm.Node):

    def __init__(self, flowchart=None, title='Energy', extension=None):
        """Initialize the node"""

        logger.debug('Creating Energy {}'.format(self))

        super().__init__(flowchart=flowchart, title=title, extension=extension)

        self.parameters = mopac_step.EnergyParameters()

        self.description = 'A single point energy calculation'
        self._long_header = ''

    @property
    def header(self):
        """A printable header for this section of output"""
        return (
            'Step {}: {}'.format(
                '.'.join(str(e) for e in self._id), self.title
            )
        )

    @property
    def version(self):
        """The semantic version of this module.
        """
        return mopac_step.__version__

    @property
    def git_revision(self):
        """The git version of this module.
        """
        return mopac_step.__git_revision__

    def description_text(self, P=None):
        """Prepare information about what this node will do
        """

        if not P:
            P = self.parameters.values_to_dict()

        text = 'Single-point energy using {hamiltonian}, converged to '
        # Convergence
        if P['convergence'] == 'normal':
            text += "the 'normal' level of 1.0e-04 kcal/mol."
        elif P['convergence'] == 'precise':
            text += "the 'precise' level of 1.0e-06 kcal/mol."
        elif P['convergence'] == 'relative':
            text += ('a factor of {relative} times the ' 'normal criterion.')
        elif P['convergence'] == 'absolute':
            text += 'converged to {absolute}'

        return self.header + '\n' + __(text, **P, indent=4 * ' ').__str__()

    def get_input(self):
        """Get the input for an energy calculation for MOPAC"""
        self._long_header = ''
        self._long_header += str(__(self.header, indent=3 * ' '))
        self._long_header += '\n'

        P = self.parameters.current_values_to_dict(
            context=seamm.flowchart_variables._data
        )
        # Have to fix formatting for printing...
        PP = dict(P)
        for key in PP:
            if isinstance(PP[key], units_class):
                PP[key] = '{:~P}'.format(PP[key])

        self._long_header += str(
            __(self.description_text(PP), **PP, indent=7 * ' ')
        )

        # Start gathering the keywords
        keywords = copy.deepcopy(P['extra keywords'])
        keywords.append('1SCF')
        keywords.append(P['hamiltonian'])

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
            raise RuntimeError(
                "Don't recognize convergence '{}'".format(P['convergence'])
            )

        # Add any extra keywords so that they appear at the end
        metadata = mopac_step.keyword_metadata
        for keyword in P['extra keywords']:
            if '=' in keyword:
                keyword, value = keyword.split('=')
                if (
                    keyword not in metadata or
                    'format' not in metadata[keyword]
                ):
                    keywords.append(keyword + '=' + value)
                else:
                    keywords.append(
                        metadata[keyword]['format'].format(keyword, value)
                    )

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
