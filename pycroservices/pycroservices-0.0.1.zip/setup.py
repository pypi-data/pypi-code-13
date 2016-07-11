#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   Copyright 2016 Satoyuki Tsukano

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from setuptools import setup

classifiers = [
   "Development Status :: 3 - Alpha",
   "License :: OSI Approved :: Apache Software License",
   "Programming Language :: Python :: 2.7",
   "Topic :: Software Development",
]

setup(
    name="pycroservices",
    version="0.0.1",
    description='pycroservices is a microservices framework on AWS Lambda.',
    license='Apache License 2.0',
    classifiers=classifiers,
    keywords=['microservices', 'AWS Lambda'],
    author='Satoyuki Tsukano',
    author_email='tknstyk at gmail.com',
    url='https://github.com/snuffkingit/pycroservices',
    install_requires=['boto3'],
    packages=[''],
)
