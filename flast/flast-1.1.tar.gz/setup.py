#!/usr/bin/env python

from os.path import join, dirname, abspath
from setuptools import setup

ROOT = dirname(abspath(__file__))

REQUIREMENTS = [
    'jinja2',
    'werkzeug'
]

def read_relative_file(filename):
    """Returns contents of the given file, whose path is supposed relative
    to this module."""
    with open(join(ROOT, filename)) as f:
        return f.read()

setup(name='flast',
      version='1.1',
      description='Werkzeug based micro-framework ',
      author='Yohann Gabory',
      author_email='yohann@gabory.fr',
      url='',
      include_package_data=True,
      scripts=['flast/bin/flast-init.py'],
      packages=['flast', 'flast.templates'],
      install_requires=REQUIREMENTS,
     )
