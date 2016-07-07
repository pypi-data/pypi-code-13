#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup
from dwlver import ver

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
    name='dwlver',
    version=ver.version,
    description="version testing",
    long_description=readme + '\n\n' + history,
    author="Matt Olsen",
    author_email='digwanderlust@gmail.com',
    url='https://github.com/digwanderlust/dwlver',
    packages=[
        'dwlver',
    ],
    package_dir={'dwlver':
                 'dwlver'},
    entry_points={
        'console_scripts': [
            'dwlver=dwlver.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="BSD license",
    zip_safe=False,
    keywords='dwlver',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
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
