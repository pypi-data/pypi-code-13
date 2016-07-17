#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'chardet',
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='textfairy',
    version='0.1.0',
    description="textfairy converts your text to UTF-8",
    long_description=readme + '\n\n' + history,
    author="Tim McNamara",
    author_email='paperless@timmcnamara.co.nz',
    url='https://git.nzoss.org.nz/tim-mcnamara/textfairy',
    packages=[
        'textfairy',
    ],
    package_dir={'textfairy':
                 'textfairy'},
    entry_points={
        'console_scripts': [
            'textfairy=textfairy.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='textfairy',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Topic :: Utilities',
        'Topic :: Text Processing :: General',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        #'Programming Language :: Python :: 3',
        #'Programming Language :: Python :: 3.3',
        #'Programming Language :: Python :: 3.4',
        #'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
