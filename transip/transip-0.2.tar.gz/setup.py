# python-transip is a Python implementation of the TransIP SOAP API
#
# Copyright (c) 2016 Nick Douma <n.douma@nekoconeko.nl>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see http://www.gnu.org/licenses/.

from setuptools import setup, find_packages
from transip.version import NAME, VERSION, DESCRIPTION

# with open('README.rst') as file:
#     long_description = file.read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    # long_description=long_description,
    author="Nick Douma",
    author_email="n.douma@nekoconeko.nl",
    url="https://github.com/LordGaav/python-transip",
    license="GPLv3",
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX :: BSD',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities'
    ],
    setup_requires=[
        "nose",
        "mock",
        "coverage"
    ],
    install_requires=[
        'suds',
        'configobj',
        'M2Crypto',
        'requests[security]',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'transip = transip.cli:main'
        ]
    }
)
