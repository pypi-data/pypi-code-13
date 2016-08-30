#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    'pytest',
]

setup(
    name='lazysecrets',
    version='0.3.0',
    description="Short description here",
    long_description=readme + '\n\n' + history,
    author="Anton Ovchinnikov",
    author_email='anton.ovchi2nikov@gmail.com',
    url='https://github.com/rev112/lazysecrets',
    packages=[
        'lazysecrets',
    ],
    package_dir={'lazysecrets':
                 'lazysecrets'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='lazysecrets',
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
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=test_requirements
)
