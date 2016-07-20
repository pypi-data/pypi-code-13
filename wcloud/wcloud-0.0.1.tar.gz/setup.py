#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'Pillow==3.3.0',
    'numpy==1.11.1',
    'wordcloud==1.2.1'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='wcloud',
    version='0.0.1',
    description="Command line tool to generate wordclouds.",
    long_description=readme + '\n\n' + history,
    author="Rafael Schultze-Kraft",
    author_email='skraftr@gmail.com',
    url='https://github.com/neocortex/wcloud',
    packages=[
        'wcloud',
    ],
    package_dir={'wcloud':
                 'wcloud'},
    entry_points={
        'console_scripts': [
            'wcloud=wcloud.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='wcloud',
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
