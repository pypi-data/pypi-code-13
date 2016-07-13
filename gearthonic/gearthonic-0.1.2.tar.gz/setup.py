#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
doclink = """
Documentation
-------------

The full documentation can be found at http://gearthonic.rtfd.org."""
changelog = open('CHANGELOG.rst').read().replace('.. :changelog:', '')

setup(
    name='gearthonic',
    version='0.1.2',
    description='A simple client to the XML RPC API of Homegear.',
    long_description=readme + '\n\n' + doclink + '\n\n' + changelog,
    author='Timo Steidle',
    author_email='mumpitz@wumpitz.de',
    url='https://gitlab.com/wumpitz/gearthonic',
    packages=[
        'gearthonic',
    ],
    package_dir={'gearthonic': 'gearthonic'},
    include_package_data=True,
    install_requires=[
    ],
    license='MIT',
    zip_safe=False,
    keywords='gearthonic',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
