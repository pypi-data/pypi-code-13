#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.app.beyonwiz',
  description = 'Beyonwiz PVR and TVWiz recording utilities',
  author = 'Cameron Simpson',
  author_email = 'cs@zip.com.au',
  version = '20160828',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 3', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)', 'Development Status :: 4 - Beta', 'Topic :: Software Development :: Libraries :: Python Modules', 'Intended Audience :: Developers', 'Operating System :: OS Independent'],
  entry_points = {'console_scripts': ['beyonwiz = cs.app.beyonwiz:main']},
  install_requires = ['cs.logutils', 'cs.obj', 'cs.threads', 'cs.urlutils'],
  keywords = ['python3'],
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.app.beyonwiz'],
)
