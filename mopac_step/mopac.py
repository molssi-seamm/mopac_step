# -*- coding: utf-8 -*-

"""Setup and run MOPAC"""

import configargparse
import cpuinfo
import logging
import seamm
import seamm.data as data
import seamm_util
import seamm_util.printing as printing
from seamm_util.printing import FormattedText as __
import mopac_step
import os
import os.path
import pprint
import re

logger = logging.getLogger(__name__)
job = printing.getPrinter()
printer = printing.getPrinter('mopac')


def upcase(string):
    """Return an uppercase version of the string.

    Used for the type argument in argparse/
    """
    return string.upper()


class MOPAC(seamm.Node):

    def __init__(
        self,
        flowchart=None,
        namespace='org.molssi.seamm.mopac',
        extension=None
    ):
        """Initialize the node"""

        logger.debug('Creating MOPAC {}'.format(self))

        # Argument/config parsing
        self.parser = configargparse.ArgParser(
            auto_env_var_prefix='',
            default_config_files=[
                '/etc/seamm/mopac.ini',
                '/etc/seamm/seamm.ini',
                '~/.seamm/mopac.ini',
                '~/.seamm/seamm.ini',
            ]
        )

        self.parser.add_argument(
            '--seamm-configfile',
            is_config_file=True,
            default=None,
            help='a configuration file to override others'
        )

        # Options for this plugin
        self.parser.add_argument(
            "--mopac-log-level",
            default=configargparse.SUPPRESS,
            choices=[
                'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'
            ],
            type=upcase,
            help="the logging level for the Mopac step"
        )

        # Options for Mopac
        self.parser.add_argument(
            '--mopac-exe',
            default='mopac',
            help='the path to the MOPAC executable'
        )

        self.parser.add_argument(
            '--mopac-num-threads',
            default='default',
            help='How many threads to use in MOPAC'
        )

        self.parser.add_argument(
            '--mopac-mkl-num-threads',
            default='default',
            help='How many threads to use with MKL in MOPAC'
        )

        self.options, self.unknown = self.parser.parse_known_args()

        # Set the logging level for this module if requested
        if 'mopac_log_level' in self.options:
            logger.setLevel(self.options.mopac_log_level)

        # Create the subflowchart and proceed
        self.subflowchart = seamm.Flowchart(
            name='MOPAC',
            namespace=namespace,
            directory=flowchart.root_directory
        )
        self._data = {}

        super().__init__(
            flowchart=flowchart,
            title='MOPAC',
            extension=extension,
            module=__name__
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

    def set_id(self, node_id):
        """Set the id for node to a given tuple"""
        self._id = node_id

        # and set our subnodes
        self.subflowchart.set_ids(self._id)

        return self.next()

    def description_text(self, P=None):
        """Return a short description of this step.

        Return a nicely formatted string describing what this step will
        do.

        Keyword arguments:
            P: a dictionary of parameter values, which may be variables
                or final values. If None, then the parameters values will
                be used as is.
        """

        # Work through children. Get the first real node
        node = self.subflowchart.get_node('1').next()

        text = self.header + '\n\n'
        while node is not None:
            text += __(node.description_text(), indent=3 * ' ').__str__()
            text += '\n'
            node = node.next()

        return text

    def run(self):
        """Run MOPAC"""
        if data.structure is None:
            logger.error('MOPAC run(): there is no structure!')
            raise RuntimeError('MOPAC run(): there is no structure!')

        # Access the options and find the executable
        o = self.options

        mopac_exe = seamm_util.check_executable(
            o.mopac_exe, key='--mopac-exe', parser=self.parser
        )

        # How many processors does this node have?
        info = cpuinfo.get_cpu_info()
        n_cores = info['count']
        # Account for Intel hyperthreading
        if info['arch'][0:3] == 'X86':
            n_cores = int(n_cores / 2)
        if n_cores < 1:
            n_cores = 1
        logger.info('The number of cores is {}'.format(n_cores))

        # Currently, on the Mac, it is not clear that any parallelism helps
        # much.
        # n_atoms = len(seamm.data.structure['atoms']['elements'])

        if o.mopac_mkl_num_threads == 'default':
            # Wild guess!
            # mopac_mkl_num_threads = int(pow(n_atoms / 16, 0.3333))
            mopac_mkl_num_threads = 1
        else:
            mopac_mkl_num_threads = int(o.mopac_mkl_num_threads)
        if mopac_mkl_num_threads > n_cores:
            mopac_mkl_num_threads = n_cores
        elif mopac_mkl_num_threads < 1:
            mopac_mkl_num_threads = 1
        logger.info('MKL will use {} threads.'.format(mopac_mkl_num_threads))

        if o.mopac_num_threads == 'default':
            # Wild guess!
            # mopac_num_threads = int(pow(n_atoms / 32, 0.5))
            mopac_num_threads = 1
            if mopac_num_threads > n_cores:
                mopac_num_threads = n_cores
        else:
            mopac_num_threads = int(o.mopac_num_threads)
        if mopac_num_threads > n_cores:
            mopac_num_threads = n_cores
        if mopac_num_threads < 1:
            mopac_num_threads = 1
        logger.info('MOPAC will use {} threads.'.format(mopac_num_threads))

        env = {
            'MKL_NUM_THREADS': str(mopac_mkl_num_threads),
            'OMP_NUM_THREADS': str(mopac_num_threads)
        }

        extra_keywords = ['AUX']

        # All Lanthanides (except La and Lu) must use the SPARKLES keyword.
        # La and Lu use the SPARKLES keyword optionally, depending
        # if you're looking for good structure (do use SPARKLES) or
        # energy (do not use SPARKLES)
        La = [
            "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er",
            "Tm", "Yb"
        ]

        La_list = set(La) & set(seamm.data.structure['atoms']['elements'])

        if len(La_list) > 0:
            extra_keywords.append("SPARKLES")

        if 'extras' in seamm.data.structure.keys():
            extras = seamm.data.structure['extras']

            for k, v in extras.items():
                if v is not None:
                    if k == 'net_charge':
                        extra_keywords.append('CHARGE={}'.format(v))
                    elif k == 'field':
                        extra_keywords.append(
                            'FIELD=({},{},{})'.format(v[0], v[1], v[2])
                        )
                    elif k == 'open':
                        extra_keywords.append('OPEN({},{})'.format(v[0], v[1]))
                    else:
                        extra_keywords.append(v)

        if mopac_num_threads > 1:
            extra_keywords.append('THREADS={}'.format(mopac_num_threads))

        # Work through the subflowchart to find out what to do.
        self.subflowchart.root_directory = self.flowchart.root_directory

        next_node = super().run(printer)

        # Get the first real node
        node = self.subflowchart.get_node('1').next()

        input_data = []
        while node:
            node.parent = self
            keywords = node.get_input()
            lines = []
            lines.append(' '.join(keywords + extra_keywords))
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

        files = {'mopac.dat': '\n'.join(input_data)}
        logger.debug('mopac.dat:\n' + files['mopac.dat'])
        os.makedirs(self.directory, exist_ok=True)
        for filename in files:
            with open(os.path.join(self.directory, filename), mode='w') as fd:
                fd.write(files[filename])
        local = seamm.ExecLocal()
        return_files = ['mopac.arc', 'mopac.out', 'mopac.aux']
        result = local.run(
            cmd=[mopac_exe, 'mopac.dat'],
            files=files,
            return_files=return_files,
            env=env
        )

        if not result:
            logger.error('There was an error running MOPAC')
            return None

        logger.debug('\n' + pprint.pformat(result))

        logger.debug(
            '\n\nOutput from MOPAC\n\n' + result['mopac.out']['data'] + '\n\n'
        )

        for filename in result['files']:
            with open(os.path.join(self.directory, filename), mode='w') as fd:
                if result[filename]['data'] is not None:
                    fd.write(result[filename]['data'])
                else:
                    fd.write(result[filename]['exception'])

        # Analyze the results
        self.analyze()

        # Close the reference handler, which should force it to close the
        # connection.
        self.references = None

        return next_node

    def analyze(self, indent='', lines=[]):
        """Read the results from MOPAC calculations and analyze them,
        putting key results into variables for subsequent use by
        other stages
        """

        # Split the aux files into sections for each step
        filename = 'mopac.aux'
        with open(os.path.join(self.directory, filename), mode='r') as fd:
            lines_aux = fd.read().splitlines()

        # Find the sections in the file corresponding to sub-tasks
        aux = []
        start = 0
        lineno = 0
        for line in lines_aux:
            if 'END OF MOPAC FILE' in line:
                aux.append((start, lineno))
            lineno += 1
            if 'START OF MOPAC FILE' in line:
                start = lineno

        # Split the output file into sections for each step
        filename = 'mopac.out'
        with open(os.path.join(self.directory, filename), mode='r') as fd:
            lines = fd.read().splitlines()

        # Find the sections in the file corresponding to sub-tasks
        out = []
        start = 0
        lineno = 0
        n_star_lines = 0
        for line in lines:
            if line[1:51] == 50 * '*':
                n_star_lines += 1
                if n_star_lines == 7:
                    out.append(lines[start:lineno])
                    start = lineno
            lineno += 1
        out.append(lines[start:])

        # Loop through our subnodes. Get the first real node
        node = self.subflowchart.get_node('1').next()
        section = 0

        for start, end in aux:
            data = self.parse_aux(lines_aux[start:end])
            logger.debug('\nAUX file section {}'.format(section))
            logger.debug('------------------')
            logger.debug(pprint.pformat(data, width=170, compact=True))

            # Add main citation for MOPAC
            if section == 1 and 'MOPAC_VERSION' in data:
                self.references.cite(
                    raw=self.bibliography['Stewart_2016'],
                    alias='mopac',
                    module='mopac_step',
                    level=1,
                    note='The principle MOPAC citation.'
                )

            node.analyze(data=data, out=out[section])

            node = node.next()
            section += 1

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

                # Check for floating point numbers run together
                if properties[name]['type'] == 'float':
                    values = []
                    for value in rest.split():
                        tmp = value.split('.')
                        if len(tmp) <= 2:
                            values.append(value)
                        else:
                            # Run together ... lets see how many decimals
                            n_decimals = len(tmp[-1])
                            # and before the decimal
                            n_digits = len(tmp[-2]) - n_decimals
                            n = n_digits + 1 + n_decimals
                            n_values = len(tmp) - 1
                            # blanks at front have been stripped, so count back
                            start = 0
                            end = len(value) - (n_values - 1) * n
                            while start < len(value):
                                values.append(value[start:end])
                                start = end
                                end += n
                    tmp = values
                else:
                    tmp = rest.split()

                # AUX file contains alpha and beta orbitals, that's why we are
                # doubling it
                if name == 'MICROSTATE_CONFIGURATIONS':
                    size = size * 2

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
                    if properties[name]['dimensionality'] == 'scalar':
                        if not (units == 'ARBITRARY_UNITS' and name in data):
                            data[name] = values[0]
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
                    value = float(self._sanitize_value(rest))
                else:
                    value = rest.strip('"')

                if 'UPDATED' in name:
                    if name not in data:
                        data[name] = []
                    data[name].append(value)
                else:
                    data[name] = value

        return data

    def _sanitize_value(self, value):
        regex = r"^([-+]?[.0-9]+)([EeDd]*)([-+][0-9]+)$"
        subs = r"\1E\3"
        ret = float(re.sub(regex, subs, value))
        return ret
