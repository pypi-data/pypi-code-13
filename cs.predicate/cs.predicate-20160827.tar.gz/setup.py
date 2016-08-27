#!/usr/bin/python
from distutils.core import setup
setup(
  name = 'cs.predicate',
  description = 'fnctions for expressing predicates',
  author = 'Cameron Simpson',
  author_email = 'cs@zip.com.au',
  version = '20160827',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  keywords = ['python2', 'python3'],
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.predicate'],
  requires = ['cs.logutils'],
)
