# -*- coding: utf-8 -*-
"""Setup and run MOPAC"""

import molssi_workflow
import molssi_workflow.data as data
import logging
import os
import os.path
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

    def set_id(self, node_id):
        """Set the id for node to a given tuple"""
        self._id = node_id

        # and set our subnodes
        self.mopac_workflow.set_ids(self._id)

        return self.next()

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
            lines.append(' '.join(keywords) + ' AUX')
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

        os.makedirs(self.directory, exist_ok=True)
        for filename in files:
            with open(os.path.join(self.directory, filename),
                      mode='w') as fd:
                fd.write(files[filename])

        local = molssi_workflow.ExecLocal()
        return_files = ['molssi.arc', 'molssi.out', 'molssi.aux']
        result = local.run(
            cmd=['mopac', 'molssi.dat'],
            files=files,
            return_files=return_files
        )

        if not result:
            logger.error('There was an error running MOPAC')
            return None

        logger.debug('\n' + pprint.pformat(result))

        logger.debug('\n\nOutput from MOPAC\n\n' +
                     result['molssi.out']['data'] + '\n\n')

        for filename in result['files']:
            with open(os.path.join(self.directory, filename), mode='w') as fd:
                if result[filename]['data'] is not None:
                    fd.write(result[filename]['data'])
                else:
                    fd.write(result[filename]['exception'])

        # Analyze the results
        self.analyze()

        return super().run()

    def analyze(self, lines=[]):
        """Read the results from MOPAC calculations and analyze them,
        putting key results into variables for subsequent use by
        other stages
        """

        filename = 'molssi.aux'
        with open(os.path.join(self.directory, filename), mode='w') as fd:
            lines = fd.read().splitlines

        # Find the sections in the file corresponding to sub-tasks
        sections = []
        lineno = 0
        for line in lines:
            if 'END OF MOPAC FILE' in line:
                sections.append((start, lineno))
            lineno += 1
            if 'START OF MOPAC FILE' in line:
                start = lineno

        # Loop through our subnodes. Get the first real node
        node = self.mopac_workflow.get_node('1').next()
        for start, end in sections:
            node.analyze(lines[start:end])
            node = node.next()
