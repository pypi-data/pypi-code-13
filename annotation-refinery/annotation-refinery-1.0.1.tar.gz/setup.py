#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import find_packages, setup


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='annotation-refinery',
    version='1.0.1',
    packages=find_packages(),
    include_package_data=True,
    url='https://bitbucket.org/greenelab/annotation-refinery',
    author='Greene Lab',
    author_email='team@greenelab.com',
    license='LICENSE.txt',
    description='Portable Python package to process publicly available ' +
        'annotated sets of genes, such as Gene Ontology and Disease Ontology' +
        'terms.',
    long_description=README,
    install_requires=[
        'argparse',
        'requests',
        'requests-ftp',
        'tribe-client',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
)
