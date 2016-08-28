#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.py3',
  description = 'Aids for code sharing between python2 and python3.',
  author = 'Cameron Simpson',
  author_email = 'cs@zip.com.au',
  version = '20160828',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Topic :: Software Development :: Libraries :: Python Modules', 'Intended Audience :: Developers', 'Development Status :: 4 - Beta', 'Operating System :: OS Independent', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = ['cs.py3_for2', 'cs.py3_for3'],
  keywords = ['python2', 'python3'],
  long_description = 'Python3 helpers to aid code sharing between python2 and python3.\n----------------------------------------------------------------\n\nPresents various names in python 3 flavour for common use in python 2 and python 3.\n',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.py3'],
)
