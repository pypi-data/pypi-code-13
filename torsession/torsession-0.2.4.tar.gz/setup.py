# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

from torsession import __version__

classifiers = """
Intended Audience :: Developers
License :: OSI Approved :: Apache Software License
Development Status :: 5 - Production/Stable
Natural Language :: English
Programming Language :: Python :: 2
Programming Language :: Python :: 2.6
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Programming Language :: Python :: 3.0
Programming Language :: Python :: 3.3
Operating System :: MacOS :: MacOS X
Operating System :: Unix
Programming Language :: Python
Programming Language :: Python :: Implementation :: CPython
"""

version = __version__
description = 'An asynchronous session backend with mongodb for tornado.'
long_description = open("README.rst").read()
packages = ['torsession']

setup(
    name='torsession',
    version=version,
    packages=packages,
    description=description,
    long_description=long_description,
    author='Lime YH.Shi',
    author_email='shiyanhui66@gmail.com',
    url='https://github.com/shiyanhui/torsession',
    license='http://www.apache.org/licenses/LICENSE-2.0',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: C",
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Compilers"
    ],
    keywords=[
        'torsession', 'mongo', 'mongodb', 'motor', 'session', 'backend',
        'tornado', 'asynchronous'
    ],
    install_requires=[
        "motor >= 0.6.2",
        "tornado >= 3.0"
    ],
    zip_safe=False,
)
