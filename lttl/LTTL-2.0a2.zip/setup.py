#!/usr/bin/env python

"""File setup.py
Copyright 2012-2016 LangTech Sarl (info@langtech.ch)
---------------------------------------------------------------------------
This file is part of the LTTL package v2.0.

LTTL v2.0 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

LTTL v2.0 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with LTTL v2.0. If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import unicode_literals

from setuptools import setup, find_packages

from codecs import open
from os import path

__version__ = "1.0.3"

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='LTTL',

    version='2.0a2',

    description='LangTech Text Library (LTTL) for text processing and analysis',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/axanthos/LTTL',

    # Author details
    author='LangTech Sarl',
    author_email='info@langtech.ch',

    # Choose your license
    license='GNU GPL v3',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing :: General',
        'Topic :: Text Processing :: Linguistic',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
    ],

    keywords=('text mining', 'text analysis', 'text processing'),

    packages=find_packages(exclude=['docs', 'tests', 'bugs']),

    install_requires=[
        'setuptools',
        'numpy',
        'future',
    ],

    test_suite='nose.collector',
    tests_require='nose',
    download_url = 'https://github.com/axanthos/LTTL/tarball/v2.0a2',
)
