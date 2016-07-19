#! /usr/bin/env python

from setuptools import find_packages, setup

setup(name='oemof.db',
      version='0.0.2',
      description='The oemof database extension',
      namespace_package = ['oemof'],
      author='oemof developing group',
      author_email='oemof@rl-institut.de',
      url='https://github.com/oemof/oemof.db',
      packages=find_packages(),
      package_dir={'oemof': 'oemof'},
      install_requires=['sqlalchemy >= 1.0',
                        'keyring >= 4.0',
                        'keyrings.alt',
                        'shapely',
                        'psycopg2'])
