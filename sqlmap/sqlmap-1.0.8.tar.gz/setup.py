#!/usr/bin/env python

"""
Copyright (c) 2006-2016 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""

from setuptools import setup, find_packages

setup(
    name='sqlmap',
    version='1.0.8',
    description="Automatic SQL injection and database takeover tool",
    author='Bernardo Damele Assumpcao Guimaraes, Miroslav Stampar',
    author_email='bernardo@sqlmap.org, miroslav@sqlmap.org',
    url='https://sqlmap.org',
    download_url='https://github.com/sqlmapproject/sqlmap/archive/1.0.8.zip',
    license='GPLv2',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'sqlmap = sqlmap.sqlmap:main',
        ],
    },
)
