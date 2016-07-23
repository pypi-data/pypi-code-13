#!/usr/bin/env python3

# Copyright 2014-2015 Louis Paternault
#
# This file is part of Jouets.
#
# Jouets is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Jouets is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Jouets.  If not, see <http://www.gnu.org/licenses/>.

"""Installer"""

from setuptools import setup, find_packages
import codecs
import glob
import os
import sys

def readme():
    """Return README string from README.rst file."""
    directory = os.path.dirname(os.path.join(
        os.getcwd(),
        __file__,
        ))
    with codecs.open(
        os.path.join(directory, "README.rst"),
        encoding="utf8",
        mode="r",
        errors="replace",
        ) as file:
        return file.read()

def get_binary_names():
    """Return the names of binaries provided by this package."""
    return [
        os.path.basename(binary)
        for binary
        in glob.glob(os.path.join(
            os.path.dirname(sys.modules['__main__'].__file__),
            'bin',
            '*'
            ))
        if not (binary == "jouets" or binary.endswith("~"))
        ]

setup(
    name='Jouets',
    version="0.2.0",
    packages=find_packages(exclude=["test*"]),
    setup_requires=["hgtools"],
    install_requires=[
        "jinja2",
        "termcolor",
        "blessings",
        ],
    include_package_data=True,
    author='Louis Paternault',
    author_email='spalax@gresille.org',
    description='Bric-à-brac de programmes mathématiques « amusants »',
    url='https://git.framasoft.org/spalax/jouets',
    license="GPLv3 or any later version",
    test_suite="test.suite",
    entry_points={
        'console_scripts': [
            "{name} = jouets.{binary}.__main__:main".format(
                name=binary.split('.')[-1],
                binary=binary,
                ) for binary in get_binary_names()
            ],
        },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Games/Entertainment",
        "Intended Audience :: Education",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Mathematics",
        ],
    long_description=readme(),
    zip_safe=False,
)
