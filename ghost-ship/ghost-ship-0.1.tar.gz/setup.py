#!/usr/bin/env python

from distutils.core import setup

setup(
  name='ghost-ship',
  version='0.1',
  description='Nomad ghost ship deploy',
  author='Thinh Tran',
  author_email='duythinht',
  url='http://git.chotot.org/corex/ghost-ship',
  packages=['ghost_ship'],
  package_data={'ghost_ship': ['templates/*.jinja']},
  py_modules=['pirate'],
  install_requires=['requests', 'python-nomad'],
  scripts=['scripts/ghost-ship']
)
