#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2015, CERN
# This software is distributed under the terms of the GNU General Public
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as Intergovernmental Organization
# or submit itself to any jurisdiction.

"""
DB On Demand REST API server setup file
"""

from setuptools import setup, find_packages

setup(name='dbod-api',
      version='0.7.8rc1',
      description='DB On Demand REST API',
      author='CERN',
      author_email='icot@cern.ch',
      license='GPLv3',
      maintainer='Ignacio Coterillo',
      maintainer_email='icot@cern.ch',
      url='https://github.com/cerndb/dbod-api',
      download_url='https://github.com/cerndb/dbod-api/archive/v0.7.3-QA.tar.gz',
      packages=find_packages(),
      scripts=['bin/dbod-api'],
      test_suite="",
      requires=[
          'ConfigParser',
          'tornado',
          'nose',
          'mock',
          'requests',
          ],
      keywords = ['cern', 'dbod', 'database', 'api'],
      classifiers = [
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 2.7',
          'Topic :: Database',
          'Development Status :: 4 - Beta',
          ]
     )
