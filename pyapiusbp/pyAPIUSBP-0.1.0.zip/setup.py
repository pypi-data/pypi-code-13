#!/usr/bin/env python
from setuptools import setup, find_packages
import sys
import os

from pyAPIUSBP import __version__

version = __version__

setup(name='pyAPIUSBP',
      version=version,
      description='Using Contec API-USBP functions from Python',
      long_description="""
pyAPIUSBP is a module for using Contec API-USBP functions 
(http://www.contec.co.jp/product/device/apiusbp/) from Python.

Disclaimer: pyAPIUSBP is unofficial. It is NOT affiliated with Contec
in any way.
""",
      classifiers=[
          # http://pypi.python.org/pypi?%3Aaction=list_classifiers
          'Development Status :: 3 - Alpha',
          'Environment :: Win32 (MS Windows)',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Operating System :: Microsoft :: Windows',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering',
      ],
      keywords='API-USBP, I/O, Digital Input, Digital Output, USB',
      author='Hiroyuki Sogo',
      author_email='hsogo@ehime-u.ac.jp',
      url='http://sourceforge.net/p/pyapiusbp/',
      license='GNU GPL',
      packages=['pyAPIUSBP'],
      package_data={'pyAPIUSBP': ['LICENSE.txt']},
      )
