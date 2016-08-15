#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='tsincluder',
    version='0.1',
    packages=['tsincluder',],
    install_requires=[
        'future',
    ],
    author='Fabien Arcellier',
    author_email='fabien.arcellier@gmail.com',
    include_package_data=True,
    entry_points = {
        'console_scripts': [
            'tsincluder = tsincluder.__main__:run',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Text Processing :: Markup'
    ],
    url='https://github.com/FabienArcellier/tsincluder',
    license='Mozilla Public License, v. 2.0',
    description="Text Script Inclusions Manager generate contents from any text file based on shell instructions",
    long_description=open('README.md').read(),
)
