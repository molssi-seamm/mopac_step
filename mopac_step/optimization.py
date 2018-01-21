# -*- coding: utf-8 -*-
"""Setup and run MOPAC"""

import logging
import mopac_step

logger = logging.getLogger(__name__)


class Optimization(mopac_step.Energy):
    def __init__(self, workflow=None, gui_object=None, title='Optimization',
                 extension=None):
        """Initialize the node"""

        logger.debug('Creating Optimization {}'.format(self))

        super().__init__(workflow=workflow, title=title, gui_object=gui_object,
                         extension=extension)

        self.description = 'A structural optimization'

    def get_input(self):
        """Get the input for an optimization MOPAC"""

        # Remove the 1SCF keyword from the energy setup
        keywords = []
        for keyword in super().get_input():
            if keyword != '1SCF':
                keywords.append(keyword)

        return keywords
