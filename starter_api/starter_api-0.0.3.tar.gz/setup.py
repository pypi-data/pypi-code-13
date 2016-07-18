#!/usr/bin/env python

import setuptools
from os import path

from starter_api import info

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

setuptools.setup(
    name=info.__package_name__,
    version=info.__version__,

    description='Client for Starter Server API',
    long_description=long_description,

    url='https://github.com/rw-meta/starter-py-client',

    author='Artur Geraschenko',
    author_email='arturgspb@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],

    setup_requires=['requests'],
    packages=["starter_api"],
    package_data={'': ['LICENSE']},
    package_dir={'starter_api': 'starter_api'},
    include_package_data=True,
)
