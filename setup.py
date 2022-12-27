#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""mopac_step
A SEAMM plug-in to setup, run and analyze semiempirical calculations with MOPAC
"""

import sys
from setuptools import setup, find_packages
import versioneer

short_description = __doc__.splitlines()[1]

# from https://github.com/pytest-dev/pytest-runner#conditional-requirement
needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as fd:
    requirements = fd.read()

setup(
    # Descriptive entries which should always be present
    name='mopac_step',
    author="Paul Saxe",
    author_email='psaxe@molssi.org',
    description=short_description,
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    license='BSD-3-Clause',
    url='https://github.com/molssi-seam/mopac_step',
    packages=find_packages(include=['mopac_step']),
    include_package_data=True,

    # Allows `setup.py test` to work correctly with pytest
    setup_requires=[] + pytest_runner,

    # Required packages, pulls from pip if needed; do not use for Conda
    # deployment
    install_requires=requirements,

    test_suite='tests',

    # Valid platforms your code works on, adjust to your flavor
    platforms=['Linux',
               'Mac OS-X',
               'Unix',
               'Windows'],

    # Manual control if final package is compressible or not, set False to
    # prevent the .egg from being made
    zip_safe=True,

    keywords=['SEAMM', 'plug-in', 'flowchart', 'forcefield', 'MOPAC',
              'semiempirical', 'orbitals'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    entry_points={
        'console_scripts': [
            'mopac-step-installer=mopac_step.__main__:run',
        ],
        'org.molssi.seamm': [
            'MOPAC = mopac_step:MOPACStep',
            'Lewis Structure = mopac_step:LewisStructureStep',
        ],
        'org.molssi.seamm.tk': [
            'MOPAC = mopac_step:MOPACStep',
            'Lewis Structure = mopac_step:LewisStructureStep',
        ],
        'org.molssi.seamm.mopac': [
            'Energy = mopac_step:EnergyStep',
            'Optimization = mopac_step:OptimizationStep',
            'IR Spectrum = mopac_step:IRStep',
            'Thermodynamics = mopac_step:ThermodynamicsStep',
            'Forceconstants = mopac_step:ForceconstantsStep',
        ],
        'org.molssi.seamm.mopac.tk': [
            'Energy = mopac_step:EnergyStep',
            'Optimization = mopac_step:OptimizationStep',
            'IR Spectrum = mopac_step:IRStep',
            'Thermodynamics = mopac_step:ThermodynamicsStep',
            'Forceconstants = mopac_step:ForceconstantsStep',
        ],
    },
)
