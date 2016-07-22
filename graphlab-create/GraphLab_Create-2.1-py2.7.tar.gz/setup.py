#!/usr/bin/env python
'''
Copyright (C) 2016 Turi
All rights reserved.

This software may be modified and distributed under the terms
of the BSD license. See the TURI-PYTHON-LICENSE file for details.
'''

import os
import sys
import glob
import subprocess
from setuptools import setup, find_packages
from setuptools.dist import Distribution
from setuptools.command.install import install

PACKAGE_NAME="graphlab"
VERSION='2.1'#{{VERSION_STRING}}


# Prevent distutils from thinking we are a pure python package
class BinaryDistribution(Distribution):
    def is_pure(self):
        return False

class InstallEngine(install):
    """Helper class to hook the python setup.py install path to download client libraries and engine"""

    def run(self):
        import platform

        # start by running base class implementation of run
        install.run(self)

        # Check correct version of architecture (64-bit only)
        arch = platform.architecture()[0]
        if arch != '64bit':
            msg = ("GraphLab Create currently supports only 64-bit operating systems, and only recent Linux/OSX " +
                   "architectures. Please install using a supported version. Your architecture is currently: %s" % arch)

            sys.stderr.write(msg)
            sys.exit(1)

        # Check correct version of Python
        if sys.version_info.major == 2 and sys.version_info[:2] < (2, 7):
            msg = ("GraphLab Create requires at least Python 2.7, please install using a supported version."
                   + " Your current Python version is: %s" % sys.version)
            sys.stderr.write(msg)
            sys.exit(1)

        # if OSX, verify > 10.7
        from distutils.util import get_platform
        from pkg_resources import parse_version
        cur_platform = get_platform()
        py_shobj_ext = 'so'

        if cur_platform.startswith("macosx"):

            mac_ver = platform.mac_ver()[0]
            if parse_version(mac_ver) < parse_version('10.8.0'):
                msg = (
                "GraphLab Create currently does not support versions of OSX prior to 10.8. Please upgrade your Mac OSX "
                "installation to a supported version. Your current OSX version is: %s" % mac_ver)
                sys.stderr.write(msg)
                sys.exit(1)
        elif cur_platform.startswith('linux'):
            pass
        elif cur_platform.startswith('win'):
            py_shobj_ext = 'pyd'
            win_ver = platform.version()
            # Verify this is Vista or above
            if parse_version(win_ver) < parse_version('6.0'):
                msg = (
                "GraphLab Create currently does not support versions of Windows"
                " prior to Vista, or versions of Windows Server prior to 2008."
                "Your current version of Windows is: %s" % platform.release())
                sys.stderr.write(msg)
                sys.exit(1)
        else:
            msg = (
                "Unsupported Platform: '%s'. GraphLab Create is only supported on Windows, Mac OSX, and Linux." % cur_platform
            )
            sys.stderr.write(msg)
            sys.exit(1)

        print ("")
        print ("")
        print ("")
        print ("NOTE:")
        print ("")
        print ("Thank you for downloading and trying GraphLab Create.")
        print ("")
        print ("GraphLab Create will send usage metrics to Turi (when you import the graphlab module) to help us make GraphLab Create better. If you would rather these metrics are not collected, please remove GraphLab Create from your system.")
        print ("")
        print ("")
        print ("")
        if not VERSION.endswith("gpu"):
            print("For Nvidia GPU CUDA support, please see https://turi.com/download/install-graphlab-create-gpu.html")

        from distutils import sysconfig
        import stat
        import glob

        root_path = os.path.join(self.install_lib, PACKAGE_NAME)

if __name__ == '__main__':
    from distutils.util import get_platform
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Other Audience",
        "Intended Audience :: Science/Research",
        "License :: Other/Proprietary License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ]
    cur_platform = get_platform()
    if cur_platform.startswith("macosx"):
        classifiers.append("Operating System :: MacOS :: MacOS X")
    elif cur_platform.startswith('linux'):
        classifiers +=  ["Operating System :: POSIX :: Linux",
                         "Operating System :: POSIX :: BSD",
                         "Operating System :: Unix"]
    elif cur_platform.startswith('win'):
        classifiers += ["Operating System :: Microsoft :: Windows"]
    else:
        msg = (
            "Unsupported Platform: '%s'. GraphLab Create is only supported on Windows, Mac OSX, and Linux." % cur_platform
            )
        sys.stderr.write(msg)
        sys.exit(1)

    setup(
        name="GraphLab-Create",
        version=VERSION,
        author='Turi',
        author_email='contact@turi.com',
        cmdclass=dict(install=InstallEngine),
        distclass=BinaryDistribution,
        package_data={
        'graphlab': ['canvas/webapp/css/*.css', 'canvas/webapp/*.html', 'canvas/webapp/*.ico',
                     'canvas/webapp/js/*.js', 'canvas/webapp/images/*.png',
                     'cython/*.so', 'cython/*.pyd', 'cython/*.dll', 'id',
                     'toolkits/deeplearning/*.conf',
                     '*.so', '*.so.1', '*.dylib',
                     '*.dll', '*.def', 'spark_unity.jar', 'distributed/*.jar',
                     'deploy/*.jar', '*.exe', 'libminipsutil.*',
                     'canvas/webapp/css/bootstrap/*.css',
                     'canvas/webapp/css/bootstrap/LICENSE',
                     'canvas/webapp/css/font-awesome/*.css',
                     'canvas/webapp/css/font-awesome/LICENSE',
                     'canvas/webapp/css/hljs/*.css',
                     'canvas/webapp/css/hljs/LICENSE',
                     'canvas/webapp/css/fixed-data-table/*.css',
                     'canvas/webapp/css/fonts/*.otf',
                     'canvas/webapp/css/fonts/*.eot',
                     'canvas/webapp/css/fonts/*.svg',
                     'canvas/webapp/css/fonts/*.ttf',
                     'canvas/webapp/css/fonts/*.woff',
                     'canvas/webapp/css/fonts/LICENSE',
                     'mxnet/*.ttf'
                     ]},
        packages=find_packages(
            exclude=["*.tests", "*.tests.*", "tests.*", "tests", "*.test", "*.test.*", "test.*", "test",
                     "*.demo", "*.demo.*", "demo.*", "demo", "*.demo", "*.demo.*", "demo.*", "demo"]),
        url='https://turi.com',
        license='LICENSE.txt',
        description='GraphLab Create enables developers and data scientists to apply machine learning to build state of the art data products.',
        # long_description=open('README.txt').read(),
        classifiers=classifiers,
        install_requires=[
            "psclient",
            "boto == 2.33.0",
            "decorator == 4.0.9",
            "tornado == 4.3",
            "prettytable == 0.7.2",
            "requests == 2.9.1",
            "awscli == 1.6.2",
            "sseclient == 0.0.8",
            "multipledispatch >= 0.4.7",
            "certifi == 2015.04.28", # we need to downgrade certifi to work with S3
            "jsonschema == 2.5.1",
            "genson == 0.1.0"
        ],
    )
