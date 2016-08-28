#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.tty',
  description = 'functions related to terminals',
  author = 'Cameron Simpson',
  author_email = 'cs@zip.com.au',
  version = '20160828',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Environment :: Console', 'Operating System :: POSIX', 'Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Topic :: Terminals', 'Intended Audience :: Developers', 'Development Status :: 4 - Beta', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  keywords = ['python2', 'python3'],
  long_description = 'Functions related to terminals.\n===============================\n\n* ttysize(fd): return a namedtuple (rows, columns) with the current terminal size; UNIX only (uses the stty command)\n',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.tty'],
)
