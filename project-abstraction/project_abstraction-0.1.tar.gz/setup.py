from __future__ import print_function
from setuptools import setup, find_packages
import os

desc = """Python script encryptor."""

AUTHOR = 'Shashwat Antony'
AUTHOR_EMAIL = 'shashwat@arya.ai'
DOWNLOAD_URL = 'http://github.com/Arya-ai/project_abstraction'
LICENSE = 'MIT'
DESCRIPTION = 'Python library for encrpting scripts'
LONG_DESCRIPTION = desc

INSTALL_REQUIRES = ['Pycrypto']

if os.path.isdir('project_abstraction'):
    with open('project_abstraction/__init__.py') as fid:
        for line in fid:
            if line.startswith('__version__'):
                VERSION = line.strip().split()[-1][1:-1]
                break

    setup(name='project_abstraction',
          version=VERSION,
          description=DESCRIPTION,
          long_description=LONG_DESCRIPTION,
          download_url=DOWNLOAD_URL,
          author=AUTHOR,
          author_email=AUTHOR_EMAIL,
          license=LICENSE,
          packages=find_packages(exclude=['tests',
                                          'tests.*',
                                          '*.tests',
                                          '*.tests.*']),
          install_requires=INSTALL_REQUIRES,
          zip_safe=False)