#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.obj',
  description = 'Convenience facilities for objects.',
  author = 'Cameron Simpson',
  author_email = 'cs@zip.com.au',
  version = '20160828',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Topic :: Software Development :: Libraries :: Python Modules', 'Intended Audience :: Developers', 'Development Status :: 4 - Beta', 'Operating System :: OS Independent', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = ['cs.py3'],
  keywords = ['python2', 'python3'],
  long_description = 'Convenience facilities for objects.\n-----------------------------------\n\nPresents:\n* flavour, for deciding whether an object resembles a mapping or sequence.\n\n* O, an object subclass with a nice __str__ and convenient __init__.\n\n* Some O_* functions for working with objects, particularly O subclasses.\n\n* Proxy, a very simple minded object proxy intened to aid debugging.\n',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.obj'],
)
