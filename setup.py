#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Pmw',
    'logging',
    'seamm',
    'pprint',
]
#    'itertools',

setup_requirements = [
    # 'pytest-runner',
    # TODO(paulsaxe): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'pytest',
    # TODO: put package test requirements here
]

setup(
    name='mopac_step',
    version='0.1.0',
    description=("A step in SEAMM for handling the semiempirical quantum "
                 "code MOPAC"),
    long_description=readme + '\n\n' + history,
    author="Paul Saxe",
    author_email='psaxe@molssi.org',
    url='https://github.com/molssi-seamm/mopac_step',
    packages=find_packages(include=['mopac_step']),
    include_package_data=True,
    install_requires=requirements,
    license="BSD license",
    zip_safe=False,
    keywords='mopac_step',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
    entry_points={
        'org.molssi.seamm': [
            'MOPAC = mopac_step:MOPACStep',
        ],
        'org.molssi.seamm.tk': [
            'MOPAC = mopac_step:MOPACStep',
        ],
        'org.molssi.seamm.mopac': [
            'Energy = mopac_step:EnergyStep',
            'Optimization = mopac_step:OptimizationStep',
            'IR Spectrum = mopac_step:IRStep',
            'Thermodynamics = mopac_step:ThermodynamicsStep',
        ],
        'org.molssi.seamm.mopac.tk': [
            'Energy = mopac_step:EnergyStep',
            'Optimization = mopac_step:OptimizationStep',
            'IR Spectrum = mopac_step:IRStep',
            'Thermodynamics = mopac_step:ThermodynamicsStep',
        ],
    },
)
