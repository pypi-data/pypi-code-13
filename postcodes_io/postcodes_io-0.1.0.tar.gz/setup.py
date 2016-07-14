#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'requests>=2.10.0',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='postcodes_io',
    version='0.1.0',
    description="Python client to connect to Postcodes.io API",
    long_description=readme + '\n\n' + history,
    author="James Ho",
    author_email='jho@neverlimited.uk',
    url='https://github.com/jimmyho/postcodes_io',
    packages=[
        'postcodes_io',
    ],
    package_dir={'postcodes_io':
                 'postcodes_io'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='postcodes_io',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        # "Programming Language :: Python :: 2",
        # 'Programming Language :: Python :: 2.6',
        # 'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
