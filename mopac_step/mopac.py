# -*- coding: utf-8 -*-
"""Setup and run MOPAC"""

import molssi_workflow
import molssi_workflow.data as data
import logging
import pprint

logger = logging.getLogger(__name__)


class MOPAC(molssi_workflow.Node):
    def __init__(self,
                 workflow=None,
                 namespace='org.molssi.workflow.mopac',
                 extension=None):
        """Initialize the node"""

        logger.debug('Creating MOPAC {}'.format(self))

        self.mopac_workflow = molssi_workflow.Workflow(
            name='MOPAC',
            namespace=namespace,
        )
        self._data = {}

        super().__init__(workflow=workflow, title='MOPAC', extension=extension)

    def run(self):
        """Run MOPAC"""

        if data.structure is None:
            logger.error('MOPAC run(): there is no structure!')
            raise RuntimeError('MOPAC run(): there is no structure!')

        # Get the first real node
        node = self.mopac_workflow.get_node('1').next()

        input_data = []
        while node:
            keywords = node.get_input()
            lines = []
            lines.append(' '.join(keywords))
            lines.append('Run from MolSSI workflow')
            lines.append('{} using {} hamiltonian'.format(
                node.description, node.hamiltonian))

            if 'OLDGEO' in keywords:
                input_data.append('\n'.join(lines))
            else:
                tmp_structure = []
                structure = molssi_workflow.data.structure
                elements = structure['atoms']['elements']
                coordinates = structure['atoms']['coordinates']
                if 'freeze' in structure['atoms']:
                    freeze = structure['atoms']['freeze']
                else:
                    freeze = [''] * len(elements)
                for element, xyz, frz in zip(elements, coordinates, freeze):
                    x, y, z = xyz
                    line = '{:2} {: 12.8f} {:d} {: 12.8f} {:d} {: 12.8f} {:d}'\
                           .format(element,
                                   x, 0 if 'x' in frz else 1,
                                   y, 0 if 'y' in frz else 1,
                                   z, 0 if 'z' in frz else 1)
                    tmp_structure.append(line)
                input_data.append('\n'.join(lines) + '\n'
                                  + '\n'.join(tmp_structure))

            node = node.next()

        files = {'molssi.dat': '\n\n'.join(input_data)}
        logger.debug('molssi.dat:\n' + files['molssi.dat'])

        local = molssi_workflow.ExecLocal()
        result = local.run(
            cmd=['mopac', 'molssi.dat'],
            files=files,
            return_files=['molssi.arc', 'molssi.out']
        )

        if not result:
            logger.error('There was an error running MOPAC')
            return None

        logger.debug('\n' + pprint.pformat(result))

        logger.info('\n\nOutput from MOPAC\n\n' +
                    result['molssi.out']['data'] + '\n\n')

        return super().run()
