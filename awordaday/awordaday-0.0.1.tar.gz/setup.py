#!/usr/bin/env python

import re

from codecs import open

from setuptools import setup


packages = [
    'awordaday',
    'awordaday.django',
]

requires = []
test_requirements = []

with open('awordaday/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()
with open('HISTORY.rst', 'r', 'utf-8') as f:
    history = f.read()

setup(
    name='awordaday',
    version=version,
    description='Adding fun to boring http headers',
    long_description=readme + '\n\n' + history,
    author='Jacques-Olivier D. Bernier',
    author_email='me@jackdbernier.com',
    url='',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    install_requires=requires,
    license='MIT',
    classifiers=(
    ),
    tests_require=test_requirements,
    extras_require={
    },
)