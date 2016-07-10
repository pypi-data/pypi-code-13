#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import find_packages, setup

templates_dir = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'itemize', 'templates')

setup(
    name = 'itemize',
    version = '0.2.4',
    packages = find_packages(),
    include_package_data = True,
    package_data = {
        os.path.join('templates', os.path.relpath(root, templates_dir)): files
        for root, dirs, files in os.walk(templates_dir)
        if '__pycache__' not in root
    },
    description = 'Itemize generates receipts.',
    author = 'Jared Contrascere',
    author_email = 'jcontra@gmail.com',
    url = 'https://github.com/libretees/itemize',
    install_requires=['jinja2', 'pycups', 'z3c.rml'],
    entry_points={
        'console_scripts': [
            'itemize = itemize.main:main',
        ]
    },
    classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Unix',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.4',
          'Topic :: Software Development',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
