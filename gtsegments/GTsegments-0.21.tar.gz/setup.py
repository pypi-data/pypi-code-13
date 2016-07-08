#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Copyright (c) 2013-2016, Philippe Bordron <philippe.bordron@gmail.com>
#
# This file is part of sgs-utils.
#
# sgs-utils is free software: you can redistribute it and/or modify
# it under the terms of the GNU LESSER GENERAL PUBLIC LICENSE as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sgs-utils is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU LESSER GENERAL PUBLIC LICENSE for more details.
#
# You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
# along with sgs-utils.  If not, see <http://www.gnu.org/licenses/>



from __future__ import absolute_import, print_function

import io
import re
import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='GTsegments',
    version='0.21',
    summary='GTsegments is a collection of python tools that computes GT segment (Genomic & Transcriptomic segments) from a genome and an unweighted coexpression graph.',
    long_description=readme(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: OS Independent',
    ],
    keywords='bioinformatics Genome Genomic Transcriptome Trancriptomic GTsegments',
    author='Philippe Bordron',
    author_email='philippe.bordron+GTsegments@gmail.com',
    license='LGPL',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(i))[0] for i in glob.glob("*.py")],
    scripts = [
        'src/gtsegments/gts.py',
    ],
    install_requires=[
        'Biopython',
        'networkx',
        'numpy',
        'progressbar2',
        'UFx',
      ],
    zip_safe=False)
