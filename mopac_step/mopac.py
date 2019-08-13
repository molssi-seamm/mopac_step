# -*- coding: utf-8 -*-

"""Setup and run MOPAC"""

import logging
import seamm
import seamm.data as data
import seamm_util.printing as printing
import mopac_step
import os
import os.path
import pprint

logger = logging.getLogger(__name__)
job = printing.getPrinter()
printer = printing.getPrinter('mopac')


class MOPAC(seamm.Node):

    def __init__(
        self,
        flowchart=None,
        namespace='org.molssi.seamm.mopac',
        extension=None
    ):
        """Initialize the node"""

        logger.debug('Creating MOPAC {}'.format(self))

        self.mopac_flowchart = seamm.Flowchart(
            name='MOPAC',
            namespace=namespace,
            directory=flowchart.root_directory
        )
        self._data = {}

        super().__init__(
            flowchart=flowchart, title='MOPAC', extension=extension
        )

    def set_id(self, node_id):
        """Set the id for node to a given tuple"""
        self._id = node_id

        # and set our subnodes
        self.mopac_flowchart.set_ids(self._id)

        return self.next()

    def describe(self, indent='', json_dict=None):
        """Write out information about what this node will do
        If json_dict is passed in, add information to that dictionary
        so that it can be written out by the controller as appropriate.
        """

        next_node = super().describe(indent, json_dict)

        # Work through children. Get the first real node
        node = self.mopac_flowchart.get_node('1').next()

        while node:
            node.describe(indent=indent + '    ', json_dict=json_dict)
            node = node.next()

        return next_node

    def run(self):
        """Run MOPAC"""

        if data.structure is None:
            logger.error('MOPAC run(): there is no structure!')
            raise RuntimeError('MOPAC run(): there is no structure!')

        next_node = super().run(printer)

        # Get the first real node
        node = self.mopac_flowchart.get_node('1').next()

        input_data = []
        while node:
            keywords = node.get_input()
            lines = []
            lines.append(' '.join(keywords) + ' AUX')
            lines.append('Run from MolSSI flowchart')
            lines.append(
                '{} using {} hamiltonian'.format(
                    node.description, node.parameters['hamiltonian']
                )
            )

            if 'OLDGEO' in keywords:
                input_data.append('\n'.join(lines))
            else:
                tmp_structure = []
                structure = seamm.data.structure
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
                input_data.append(
                    '\n'.join(lines) + '\n' + '\n'.join(tmp_structure) + '\n'
                )

            node = node.next()

        files = {'molssi.dat': '\n'.join(input_data)}
        logger.debug('molssi.dat:\n' + files['molssi.dat'])

        os.makedirs(self.directory, exist_ok=True)
        for filename in files:
            with open(os.path.join(self.directory, filename), mode='w') as fd:
                fd.write(files[filename])

        local = seamm.ExecLocal()
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

        logger.debug(
            '\n\nOutput from MOPAC\n\n' + result['molssi.out']['data'] + '\n\n'
        )

        for filename in result['files']:
            with open(os.path.join(self.directory, filename), mode='w') as fd:
                if result[filename]['data'] is not None:
                    fd.write(result[filename]['data'])
                else:
                    fd.write(result[filename]['exception'])

        # Analyze the results
        self.analyze()

        return next_node

    def analyze(self, indent='', lines=[]):
        """Read the results from MOPAC calculations and analyze them,
        putting key results into variables for subsequent use by
        other stages
        """

        filename = 'molssi.aux'
        with open(os.path.join(self.directory, filename), mode='r') as fd:
            lines = fd.read().splitlines()

        # Find the sections in the file corresponding to sub-tasks
        sections = []
        start = 0
        lineno = 0
        for line in lines:
            if 'END OF MOPAC FILE' in line:
                sections.append((start, lineno))
            lineno += 1
            if 'START OF MOPAC FILE' in line:
                start = lineno

        # Loop through our subnodes. Get the first real node
        node = self.mopac_flowchart.get_node('1').next()
        section = 0
        for start, end in sections:
            section += 1
            data = self.parse_aux(lines[start:end])

            logger.debug('\nAUX file section {}'.format(section))
            logger.debug('------------------')
            logger.debug(pprint.pformat(data, width=170, compact=True))

            node.analyze(data=data)

            node = node.next()

        printer.normal('')

    def parse_aux(self, lines):
        """Digest a section of the aux file"""

        properties = mopac_step.properties
        trans = str.maketrans('Dd', 'Ee')

        data = {}
        lineno = -1
        nlines = len(lines)
        while True:
            lineno += 1
            if lineno >= nlines:
                break
            line = lines[lineno].strip()
            if line[0] == "#":
                continue
            if '=' not in line:
                raise RuntimeError(
                    "Problem parsing MOPAC aux file: '" + line + "'"
                )
            key, rest = line.split('=', maxsplit=1)
            if key[-1] == ']':
                name, size = key[0:-1].split('[')
                size = int(size.lstrip('0'))
                if ':' in name:
                    name, units = name.split(':')

                if name not in properties:
                    raise RuntimeError(
                        "Property '{}' not recognized.".format(name)
                    )
                if 'units' in properties[name]:
                    data[name + ',units'] = properties[name]['units']

                tmp = rest.split()
                while len(tmp) < size:
                    lineno += 1
                    line = lines[lineno].strip()
                    if line[0] != '#':
                        tmp.extend(line.split())
                if properties[name]['type'] == 'integer':
                    values = []
                    for value in tmp:
                        values.append(int(value))
                elif properties[name]['type'] == 'float':
                    values = []
                    for value in tmp:
                        values.append(float(value.translate(trans)))
                else:
                    values = tmp

                if 'UPDATED' in name:
                    if name not in data:
                        data[name] = []
                    data[name].append(values)
                else:
                    data[name] = values
            else:
                if ':' in key:
                    name, units = key.split(':')
                else:
                    name = key

                if name not in properties:
                    raise RuntimeError(
                        "Property '{}' not recognized.".format(name)
                    )
                if 'units' in properties[name]:
                    data[name + ',units'] = properties[name]['units']

                if properties[name]['type'] == 'integer':
                    value = int(rest)
                elif properties[name]['type'] == 'float':
                    value = float(rest.translate(trans))
                else:
                    value = rest.strip('"')

                if 'UPDATED' in name:
                    if name not in data:
                        data[name] = []
                    data[name].append(value)
                else:
                    data[name] = value
        return data
