# -*- coding: utf-8 -*-

"""
.. module:: setup.py

   :license: GPL / CeCILL
   :platform: Unix
   :synopsis: dreq setup.

.. moduleauthor:: Mark Conway-Greenslade (momipsl@ipsl.jussieu.fr)

"""
import os
import re
import codecs

from setuptools import setup
from setuptools import find_packages
from setuptools.dist import Distribution


# List of 3rd party python dependencies.
_REQUIRES = []


class _BinaryDistribution(Distribution):
    """Distribution sub-class to override defaults.

    """
    def is_pure(self):
        """Gets flag indicating whether build is pure python or not.

        """
        return False


def _read(fname):
    """Returns content of a file.

    """
    fpath = os.path.dirname(__file__)
    fpath = os.path.join(fpath, fname)
    with codecs.open(fpath, 'r', 'utf-8') as file_:
        return file_.read()


def _get_version():
    """Returns library version by inspecting __init__.py file.

    """
    return re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                     _read("dreq/__init__.py"),
                     re.MULTILINE).group(1)


# Libary version.
_VERSION = _get_version()

# Library packages.
_PACKAGES = find_packages()

# User readme.
_README = _read('README.rst')



setup(
    name='dreq',
    version=_VERSION,
    description='dreq is a light weight python client for interacting with the data request.',
    long_description=_README,
    author='Mark A. Greenslade',
    author_email='momipsl@ipsl.jussieu.fr',
    url='https://github.com/Prodiguer/prodiguer-dreq',
    packages=_PACKAGES,
    include_package_data=True,
    install_requires=_REQUIRES,
    license='GPL',
    zip_safe=False,
    distclass=_BinaryDistribution,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'License :: OSI Approved :: CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
