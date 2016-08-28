#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.range',
  description = 'a Range class implementing compact integer ranges with a set-like API, and associated functions',
  author = 'Cameron Simpson',
  author_email = 'cs@zip.com.au',
  version = '20160828',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Topic :: Software Development :: Libraries :: Python Modules', 'Intended Audience :: Developers', 'Development Status :: 4 - Beta', 'Operating System :: OS Independent', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = ['cs.logutils'],
  keywords = ['python2', 'python3'],
  long_description = 'Compact integer ranges with a set-like API\n==========================================\n\nA Range is used to represent integer ranges, such a file offset spans.\n\nMuch of the set API is presented to modify and test Ranges, looking somewhat like sets of intergers but extended slightly to accept ranges as well as individual integers so that one may say "R.add(start, end)" and so forth.\n\nAlso provided:\n\n* Span, a simple start:end range.\n\n* overlap: return the overlap of two Spans\n\n* spans: return an iterable of Spans for all contiguous sequences in the ordered integers supplied\n',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.range'],
)
