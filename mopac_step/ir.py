# -*- coding: utf-8 -*-
"""Setup and run MOPAC"""

import logging
import mopac_step

logger = logging.getLogger(__name__)


class IR(mopac_step.Energy):
    def __init__(self, workflow=None, title='IR Spectrum', extension=None):
        """Initialize the node"""

        logger.debug('Creating IR {}'.format(self))

        super().__init__(workflow=workflow, title=title, extension=extension)

        self.description = 'Infrared (vibrational) spectroscopy calculation'

    def get_input(self):
        """Get the input for an optimization MOPAC"""

        # Remove the 1SCF keyword from the energy setup
        keywords = []
        for keyword in super().get_input():
            if keyword == '1SCF':
                keywords.append('FORCE')
            else:
                keywords.append(keyword)

        return keywords
