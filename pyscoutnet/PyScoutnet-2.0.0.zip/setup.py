'''
Copyright (c) 2016, Jan Brohl <janbrohl@t-online.de>.
All rights reserved.
See LICENSE.txt
'''
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

from setuptools import setup
import pyscoutnet

name = "PyScoutnet"
url = "https://bitbucket.org/janbrohl/" + name.lower()

setup(name=name,
      version=pyscoutnet.__version__,
      author="Jan Brohl",
      author_email="janbrohl@t-online.de",
      url=url,
      package_dir={"": "src"},
      data_files=["LICENSE.txt", "src/api_examples.py"],
      packages=["pyscoutnet"],
      requires=["requests"],
      test_suite='tests',
      description="Access to the Scoutnet.de REST-API",
      license="BSD-3-Clause",
      classifiers=[
          "Intended Audience :: Developers",
          "Development Status :: 4 - Beta",
          "License :: OSI Approved :: BSD License",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.2",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
      ]
      )
