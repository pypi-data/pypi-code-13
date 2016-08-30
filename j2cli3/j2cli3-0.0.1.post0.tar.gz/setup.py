#!/usr/bin/env python
"""
j2cli
==========

Command-line interface to [Jinja2](http://jinja.pocoo.org/docs/) for templating in shell scripts.

Features:

* Jinja2 templating supporting python 3.x with better UTF8 support
* Allows to use environment variables! Hello [Docker](http://www.docker.com/) :)
* INI, YAML, JSON data sources supported

Inspired by [kolypto/jinja2-cli](https://github.com/kolypto/jinja2-cli)
"""

from setuptools import setup, find_packages

setup(
    name='j2cli3',
    version='0.0.1-0',
    author='Jun Jing Zhang',
    author_email='zhangjunjing@gmail.com',

    url='https://github.com/jjzhang/j2cli',
    license='BSD',
    description='Command-line interface to Jinja2 for templating in shell scripts.',
    long_description=__doc__,
    keywords=['Jinja2', 'templating', 'command-line', 'CLI'],

    packages=find_packages(),
    scripts=[],
    entry_points={
        'console_scripts': [
            'j2 = j2cli:main',
        ]
    },

    install_requires=[
        'jinja2 >= 2.7.2',
    ],
    extras_require={
        'yaml': ['pyyaml',]
    },
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',

    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        #'Programming Language :: Python :: 3',
    ],
)
