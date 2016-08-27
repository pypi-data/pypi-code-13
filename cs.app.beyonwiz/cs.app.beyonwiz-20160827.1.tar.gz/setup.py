#!/usr/bin/python
from distutils.core import setup
setup(
  name = 'cs.app.beyonwiz',
  description = 'Beyonwiz PVR and TVWiz recording utilities',
  author = 'Cameron Simpson',
  author_email = 'cs@zip.com.au',
  version = '20160827.1',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 3', 'Intended Audience :: Developers', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)', 'Development Status :: 4 - Beta', 'Operating System :: OS Independent'],
  entry_points = {'console_scripts': ['beyonwiz = cs.app.beyonwiz:main']},
  keywords = ['python3'],
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.app.beyonwiz'],
  requires = ['cs.logutils', 'cs.obj', 'cs.threads', 'cs.urlutils'],
)
