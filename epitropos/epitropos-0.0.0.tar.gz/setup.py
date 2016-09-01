# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

import os
import sys
sys.path.insert(0, os.path.abspath('src/'))

import epitropos  # noqa


setup(
    name='epitropos',
    version=epitropos.__version__,
    description='Fabulously simple OAuth2 server with pluggable storage '
                'and authentication plugins.',

    url='https://glow.dev.ramcloud.io/sjohnson/epitropos',
    author='Sean Johnson',
    author_email='pirogoeth@maio.me',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Bottle',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: System :: Systems Administration :: Authentication/Directory',
        'Topic :: System :: Systems Administration :: Authentication/Directory :: LDAP',
    ],
    packages=find_packages('src'),
    package_dir={
        '': 'src'
    },
    install_requires=[
        'malibu',
    ],
    include_package_data=True,
    exclude_package_data={
        '': ['README.md'],
    },
    entry_points={
        'console_scripts': [
            'epictl = epitropos.cmd.console:command_main',
        ],
    },
    test_suite='nose.collector',
    tests_require=[
        'nose',
        'coverage',
    ],
    zip_safe=True
)
