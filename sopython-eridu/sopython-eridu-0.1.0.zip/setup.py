#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

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
    name='sopython-eridu',
    version='0.1.0',
    description="Project Cradle library for accessing historic SO content.",
    long_description=readme + '\n\n' + history,
    author="Keiron J. Pizzey",
    author_email='kjpizzey@gmail.com',
    url='https://github.com/ffisegydd/eridu',
    packages=[
        'eridu',
    ],
    package_dir={'eridu':
                 'eridu'},
    entry_points={
        'console_scripts': [
            'eridu=eridu.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="BSD license",
    zip_safe=False,
    keywords='eridu',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
