#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages

import os
import re
import codecs


def read_version():
    version_file = codecs.open(
            os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                'epiclient/__init__.py'),
            'r', 'utf-8').read()
    return re.search(
            r"^__version__ = ['\"]([^'\"]*)['\"]",
            version_file, re.M).group(1)

version = read_version()


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'arrow',
    'boto3',
    'Click>=6.0',
    'epipearl>=0.2.0',
    'Jinja2',
    'json-spec',
    'python-dotenv',
    'requests'
]

test_requirements = [
    'pytest',
    'mock',
]

setup(
    name='epiclient',
    version=version,
    description="dce client for epipearl",
    long_description=readme + '\n\n' + history,
    author="nmaekawa",
    author_email='nmaekawa@g.harvard.edu',
    url='https://github.com/harvard-dce/epiclient',
    packages=find_packages(exclude=["docs", "tests*"]),
    package_dir={'epiclient':
                 'epiclient'},
    entry_points={
        'console_scripts': [
            'epiclient=epiclient.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license='Apache Software License 2.0',
    zip_safe=False,
    keywords='epiclient',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
