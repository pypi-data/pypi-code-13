#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from setuptools import setup, find_packages
 

import anonymizer
 
setup(
 
    name='anonymizer',
 
    version=anonymizer.__version__,
 
    packages=find_packages(),
 
    author="SGMAP-AGD",
 

    author_email="pierre-louis.bithorel@data.gouv.fr",
 
    description="Anonymisation de bases de données à caractère personnel",
 
    long_description=open('README.md').read(),
 

    include_package_data=True,
 

    url='https://github.com/SGMAP-AGD/anonymisation',
 

    classifiers=[
        "Programming Language :: Python",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.3",
	"License :: OSI Approved :: GNU General Public License (GPL)",
    ],


    entry_points = {
        'console_scripts': [
            'get_k = anonymizer.anonymity:get_k',
            'local_aggregation = anonymizer.anonymity:local_aggregation',
        ],
    },
 
 

 
)
