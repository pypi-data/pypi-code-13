#! /usr/bin/env python
"""Setup script for Operalib."""
# Copyright (C) 2007-2009 Cournapeau David <cournape@gmail.com>
#               2010 Fabian Pedregosa <fabian.pedregosa@inria.fr>
#
# Adapted for operalib:
# Copyright (C) 2015 Romain Brault <romain.brault@telecom-paristech.fr>
# License: 3-clause BSD

import sys
import os
import subprocess
import shutil

from setuptools import find_packages
from distutils.command.clean import clean as Clean
from pkg_resources import parse_version

if sys.version_info[0] < 3:
    import __builtin__ as builtins
else:
    import builtins

# This is a bit (!) hackish: we are setting a global variable so that the main
# operalib __init__ can detect if it is being loaded by the setup routine, to
# avoid attempting to load components that aren't built yet:
# the numpy distutils extensions that are used by operalib to recursively
# build the compiled extensions in sub-packages is based on the Python import
# machinery.
builtins.__OPERALIB_SETUP__ = True

DISTNAME = 'operalib'
DESCRIPTION = 'A python module for learnign with operator-valued kernels'
with open('README.rst') as f:
    LONG_DESCRIPTION = f.read()
MAINTAINER = 'Romain Brault'
MAINTAINER_EMAIL = 'romain.brault@telecom-paristech.fr'
URL = 'http://operalib.github.io/operalib/documentation/'
LICENSE = 'MIT'
DOWNLOAD_URL = 'https://github.com/operalib/operalib/'

import operalib

VERSION = operalib.__version__

with open('requirements.txt') as f:
    INSTALL_REQUIRES = [l.strip() for l in f.readlines() if l]

# Optional setuptools features
# We need to import setuptools early, if we want setuptools features,
# as it monkey-patches the 'setup' function
# For some commands, use setuptools
SETUPTOOLS_COMMANDS = set([
    'develop', 'release', 'bdist_egg', 'bdist_rpm',
    'bdist_wininst', 'install_egg_info', 'build_sphinx',
    'egg_info', 'easy_install', 'upload', 'bdist_wheel',
    '--single-version-externally-managed',
])
if SETUPTOOLS_COMMANDS.intersection(sys.argv):
    extra_setuptools_args = dict(
        zip_safe=False,  # the package can run out of an .egg file
        include_package_data=True,
    )
else:
    extra_setuptools_args = dict()


# Custom clean command to remove build artifacts
class CleanCommand(Clean):
    description = "Remove build artifacts from the source tree"

    def run(self):
        Clean.run(self)
        # Remove c files if we are not within a sdist package
        cwd = os.path.abspath(os.path.dirname(__file__))
        remove_c_files = not os.path.exists(os.path.join(cwd, 'PKG-INFO'))
        if remove_c_files:
            cython_hash_file = os.path.join(cwd, 'cythonize.dat')
            if os.path.exists(cython_hash_file):
                os.unlink(cython_hash_file)
            print('Will remove generated .c files')
        if os.path.exists('build'):
            shutil.rmtree('build')
        for dirpath, dirnames, filenames in os.walk('operalib'):
            for filename in filenames:
                if any(filename.endswith(suffix) for suffix in
                       (".so", ".pyd", ".dll", ".pyc")):
                    os.unlink(os.path.join(dirpath, filename))
                    continue
                extension = os.path.splitext(filename)[1]
                if remove_c_files and extension in ['.c', '.cpp']:
                    pyx_file = str.replace(filename, extension, '.pyx')
                    if os.path.exists(os.path.join(dirpath, pyx_file)):
                        os.unlink(os.path.join(dirpath, filename))
            for dirname in dirnames:
                if dirname == '__pycache__':
                    shutil.rmtree(os.path.join(dirpath, dirname))

cmdclass_operalib = {'clean': CleanCommand}

# Optional wheelhouse-uploader features
# To automate release of binary packages for operalib we need a tool
# to download the packages generated by travis and appveyor workers (with
# version number matching the current release) and upload them all at once
# to PyPI at release time.
# The URL of the artifact repositories are configured in the setup.cfg file.

WHEELHOUSE_UPLOADER_COMMANDS = set(['fetch_artifacts', 'upload_all'])
if WHEELHOUSE_UPLOADER_COMMANDS.intersection(sys.argv):
    import wheelhouse_uploader.cmd

    cmdclass_operalib.update(vars(wheelhouse_uploader.cmd))


def configuration(parent_package='', top_path=None):
    if os.path.exists('MANIFEST'):
        os.remove('MANIFEST')

    from numpy.distutils.misc_util import Configuration
    config = Configuration(None, parent_package, top_path)

    # Avoid non-useful msg:
    # "Ignoring attempt to set 'name' (from ... "
    config.set_options(ignore_setup_xxx_py=True,
                       assume_default_configuration=True,
                       delegate_options_to_subpackages=True,
                       quiet=True)

    config.add_subpackage('operalib')

    return config


scipy_min_version = '0.9'
numpy_min_version = '1.6.1'


def get_scipy_status():
    """
    Return a dictionary containing a boolean specifying whether SciPy
    is up-to-date, along with the version string (empty string if
    not installed).
    """
    scipy_status = {}
    try:
        import scipy
        scipy_version = scipy.__version__
        scipy_status['up_to_date'] = parse_version(
            scipy_version) >= parse_version(scipy_min_version)
        scipy_status['version'] = scipy_version
    except ImportError:
        scipy_status['up_to_date'] = False
        scipy_status['version'] = ""
    return scipy_status


def get_numpy_status():
    """
    Return a dictionary containing a boolean specifying whether NumPy
    is up-to-date, along with the version string (empty string if
    not installed).
    """
    numpy_status = {}
    try:
        import numpy
        numpy_version = numpy.__version__
        numpy_status['up_to_date'] = parse_version(
            numpy_version) >= parse_version(numpy_min_version)
        numpy_status['version'] = numpy_version
    except ImportError:
        numpy_status['up_to_date'] = False
        numpy_status['version'] = ""
    return numpy_status


def generate_cython():
    cwd = os.path.abspath(os.path.dirname(__file__))
    print("Cythonizing sources")
    p = subprocess.call([sys.executable, os.path.join(cwd,
                                                      'build_tools',
                                                      'cythonize.py'),
                         'operalib'],
                        cwd=cwd)
    if p != 0:
        raise RuntimeError("Running cythonize failed!")


def setup_package():
    metadata = dict(name=DISTNAME,
                    maintainer=MAINTAINER,
                    maintainer_email=MAINTAINER_EMAIL,
                    description=DESCRIPTION,
                    license=LICENSE,
                    url=URL,
                    version=VERSION,
                    packages=find_packages(),
                    install_requires=INSTALL_REQUIRES,
                    download_url=DOWNLOAD_URL,
                    long_description=LONG_DESCRIPTION,
                    classifiers=['Intended Audience :: Science/Research',
                                 'Intended Audience :: Developers',
                                 'License :: OSI Approved',
                                 'Programming Language :: C',
                                 'Programming Language :: Python',
                                 'Topic :: Software Development',
                                 'Topic :: Scientific/Engineering',
                                 'Operating System :: Microsoft :: Windows',
                                 'Operating System :: POSIX',
                                 'Operating System :: Unix',
                                 'Operating System :: MacOS',
                                 'Programming Language :: Python :: 2',
                                 'Programming Language :: Python :: 2.7',
                                 'Programming Language :: Python :: 3',
                                 'Programming Language :: Python :: 3.5',
                                 ],
                    cmdclass=cmdclass_operalib,
                    **extra_setuptools_args)

    if len(sys.argv) == 1 or (
            len(sys.argv) >= 2 and ('--help' in sys.argv[1:] or
                                    sys.argv[1] in ('--help-commands',
                                                    'egg_info',
                                                    '--version',
                                                    'clean'))):
        # For these actions, NumPy is not required, nor Cythonization
        #
        # They are required to succeed without Numpy for example when
        # pip is used to install operalib when Numpy is not yet present in
        # the system.
        try:
            from setuptools import setup
        except ImportError:
            from distutils.core import setup

        metadata['version'] = VERSION
    else:
        numpy_status = get_numpy_status()
        numpy_req_str = "operalib requires NumPy >= {0}.\n".format(
            numpy_min_version)
        scipy_status = get_scipy_status()
        scipy_req_str = "operalib requires SciPy >= {0}.\n".format(
            scipy_min_version)

        instructions = ("Installation instructions are available on the "
                        "operalib website: "
                        "http://operalib.github.io/"
                        "operalib/documentation/\n")

        if numpy_status['up_to_date'] is False:
            if numpy_status['version']:
                raise ImportError("Your installation of Numerical Python "
                                  "(NumPy) {0} is out-of-date.\n{1}{2}"
                                  .format(numpy_status['version'],
                                          numpy_req_str, instructions))
            else:
                raise ImportError("Numerical Python (NumPy) is not "
                                  "installed.\n{0}{1}"
                                  .format(numpy_req_str, instructions))
        if scipy_status['up_to_date'] is False:
            if scipy_status['version']:
                raise ImportError("Your installation of Scientific Python "
                                  "(SciPy) {0} is out-of-date.\n{1}{2}"
                                  .format(scipy_status['version'],
                                          scipy_req_str, instructions))
            else:
                raise ImportError("Scientific Python (SciPy) is not "
                                  "installed.\n{0}{1}"
                                  .format(scipy_req_str, instructions))

        from numpy.distutils.core import setup

        metadata['configuration'] = configuration

        if len(sys.argv) >= 2 and sys.argv[1] not in 'config':
            # Cythonize if needed

            print('Generating cython files')
            cwd = os.path.abspath(os.path.dirname(__file__))
            if not os.path.exists(os.path.join(cwd, 'PKG-INFO')):
                # Generate Cython sources, unless building from source release
                generate_cython()

            # Clean left-over .so file
            for dirpath, dirnames, filenames in os.walk(
                    os.path.join(cwd, 'operalib')):
                for filename in filenames:
                    extension = os.path.splitext(filename)[1]
                    if extension in (".so", ".pyd", ".dll"):
                        pyx_file = str.replace(filename, extension, '.pyx')
                        print(pyx_file)
                        if not os.path.exists(os.path.join(dirpath, pyx_file)):
                            os.unlink(os.path.join(dirpath, filename))

    setup(**metadata)


if __name__ == "__main__":
    setup_package()
