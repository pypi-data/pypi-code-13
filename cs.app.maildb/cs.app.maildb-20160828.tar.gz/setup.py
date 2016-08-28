#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.app.maildb',
  description = 'a cs.nodedb NodeDB subclass for storing email address information (groups, addresses, so forth)',
  author = 'Cameron Simpson',
  author_email = 'cs@zip.com.au',
  version = '20160828',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)', 'Development Status :: 4 - Beta', 'Topic :: Software Development :: Libraries :: Python Modules', 'Intended Audience :: Developers', 'Operating System :: OS Independent'],
  entry_points = {'console_scripts': ['maildb = cs.app.maildb:main']},
  install_requires = ['cs.logutils', 'cs.mailutils', 'cs.nodedb', 'cs.lex', 'cs.seq', 'cs.sh', 'cs.threads', 'cs.py.func', 'cs.py3'],
  keywords = ['python2', 'python3'],
  long_description = 'MailDB: NodeDB subclass for storing email information.\n======================================================\n\nA MailDB is a subclass of the NodeDB from cs.nodedb_; I use it to manage my mail address database and groups (which are consulted by `my mailfiling system`_ and also used to generate mail aliases).\n\nIt comes with a script named "maildb" for editing the database and performing various routine tasks such as learning all the addresses from a mail message or emitting mail alias definitions, particularly for mutt_.\n\nA MailDB knows about an assortment of Node types and has Node subclasses for these with convenience methods for suitable tasks; creating a Node with a the type "ADDRESS", for example, instantiates an AddressNode.\n\n.. _cs.nodedb: https://pypi.python.org/pypi/cs.nodedb\n.. _mutt: http://www.mutt.org/\n.. _my mailfiling system: https://pypi.python.org/pypi/cs.app.mailfiler\n',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.app.maildb'],
)
