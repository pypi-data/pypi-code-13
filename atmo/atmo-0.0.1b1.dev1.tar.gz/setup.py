#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='atmo',
    version=__import__("atmo").__version__,
    packages=find_packages(),
    author="Olivier Watte",
    author_email="owatte@emnet.cc",

    description='Current Guadeloupe (French West Indies) '
                'ATMO pollution indicator (from 1 to 10)',
    long_description=open('README.md').read(),

    include_package_data=True,
    url='https://github.com/Alert-Box/atmo',

    # https://pypi.python.org/pypi?%3Aaction=list_classifiers.
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        " ".join(["License :: OSI Approved :: GNU Lesser General Public",
                  "License v3 or later (LGPLv3+)"]),
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Utilities",
    ],
    entry_points={
        'console_scripts': [
            'atmo = atmo.atmo:run',
        ],
    },
)
