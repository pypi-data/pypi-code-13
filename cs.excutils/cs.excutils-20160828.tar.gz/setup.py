#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.excutils',
  description = 'Convenience facilities for managing exceptions.',
  author = 'Cameron Simpson',
  author_email = 'cs@zip.com.au',
  version = '20160828',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)', 'Development Status :: 4 - Beta', 'Topic :: Software Development :: Libraries :: Python Modules', 'Intended Audience :: Developers', 'Operating System :: OS Independent'],
  keywords = ['python2', 'python3'],
  long_description = 'Convenience facilities for managing exceptions.\n-----------------------------------------------\n\nPresents:\n\n* return_exc_info: call supplied function with arguments, return either (function_result, None) or (None, exc_info) if an exception was raised.\n\n* @returns_exc_info, a decorator for a function which wraps in it return_exc_info.\n\n* @noexc, a decorator for a function whose exceptions should never escape; instead they are logged. The initial use case was inside logging functions, where I have had a failed logging action abort a program. Obviously this is a decorator which should see very little use.\n\n* @noexc_gen, a decorator for generators with similar effect to @noexc for ordinary functions.\n',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.excutils'],
)
