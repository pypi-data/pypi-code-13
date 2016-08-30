#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

import randgen_maptools

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='randgen_maptools',
    version=randgen_maptools.__version__,
    description="Core map tools for randgen.io map generators.",
    long_description=readme + '\n\n' + history,
    author="Dan Alexander",
    author_email='lxndrdagreat@gmail.com',
    url='https://github.com/lxndrdagreat/randgen_maptools',
    packages=[
        'randgen_maptools',
    ],
    package_dir={'randgen_maptools':
                 'randgen_maptools'},
    entry_points={
        'console_scripts': [
            'randgen_maptools=randgen_maptools.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='randgen_maptools',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
