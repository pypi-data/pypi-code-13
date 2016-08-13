#!/usr/bin/env python
# coding: utf8

from setuptools import setup

install_requires = [
    'tornado',
    'xtls',
    'pymongo'
]

entry_points = {
    'console_scripts': [
        'xmemx=apps.main:main',
    ]
}


setup(
    name='xmemx',
    version='0.0.2',
    url='http://xmemx.com',
    license='GPLv3',
    description="xmemx.",
    author='i@xlzd.me',
    packages=['apps'],
    # package_dir={'': 'apps'},
    install_requires=install_requires,
    entry_points=entry_points
)
