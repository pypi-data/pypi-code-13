#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.rfc2616',
  description = 'RFC2616 (HTTP 1.1) facilities',
  author = 'Cameron Simpson',
  author_email = 'cs@zip.com.au',
  version = '20160828',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 3', 'Topic :: Software Development :: Libraries :: Python Modules', 'Intended Audience :: Developers', 'Development Status :: 4 - Beta', 'Operating System :: OS Independent', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = ['cs.fileutils', 'cs.lex', 'cs.logutils', 'cs.timeutils'],
  keywords = ['python3'],
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.rfc2616'],
)
