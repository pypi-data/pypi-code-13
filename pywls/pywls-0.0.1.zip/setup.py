#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.insert(0, os.path.abspath('lib'))

from pywls.release import __version__, __author__

try:
    from setuptools import setup, find_packages
except ImportError, e:
    print("PyWLS now needs setuptools in order to build. Install it using"
          " your package manager (usually python-setuptools) or via pip (pip"
          " install setuptools).")

setup(
    name='pywls',
    version=__version__,
    description="Weblogic automation with Python",
    author="Ethn Chao",
    author_email='maicheng.linyi@gmail.com',
    url='https://github.com/ethnchao/pywls',
    package_dir={'': 'lib'},
    packages=find_packages('lib'),
    include_package_data=True,
    install_requires=['setuptools'],
    license="GPLv3",
    keywords='pywls python weblogic ansible',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    scripts=[
        'bin/pywls',
        'bin/pywls-play',
    ],
    test_suite='tests',
    tests_require=['setuptools'],
)
