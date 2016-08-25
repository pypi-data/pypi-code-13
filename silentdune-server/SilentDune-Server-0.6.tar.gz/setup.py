#
# Authors: Robert Abram <robert.abram@entpack.com>
#
# Copyright (C) 2015 EntPack
# see file 'LICENSE' for use and warranty information
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import sys
from distutils.core import setup
from setuptools import find_packages

__VERSION__ = "0.6"


def find_package_data_files(dirs):
    paths = []
    for directory in dirs:
        for (path, directories, filenames) in os.walk(directory):
            for filename in filenames:
                paths.append(os.path.join('..', path, filename))
    return paths


def setup_package():

    # Recursively gather all non-python module directories to be included in packaging.
    core_files = find_package_data_files([
    ])

    setup(name='SilentDune-Server',
        version=__VERSION__,
        description='Silent Dune Server',
        author='Robert Abram',
        author_email='robert.abram@entpack.com',
        url='https://github.com/EntPack/SilentDune',
        packages=find_packages(exclude=['tests']),
        package_data={
            'silentdune_server': core_files,
        },
        keywords=['firewall', 'security'],  # arbitrary keywords
        classifiers=[
            'Development Status :: 4 - Beta',
            'Programming Language :: Python',
            'Environment :: Console',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Operating System :: POSIX :: Linux',
        ],

        install_requires=[
            'django',
            'django-oauth-toolkit',
            'djangorestframework',
            'django-compressor',
            'django-celery',
            'django-celery-with-redis',
            'django-countries',
            'django-axes',
            'django-filter',
            'cryptography',
            'mysqlclient',
            'requests',
            'raven',
            'sqlparse',
        ],

        tests_require=[
            'pytest',
            'pytest-runner',
            'pytest-pythonpath',
        ],
     )

if __name__ == "__main__":
    setup_package()
