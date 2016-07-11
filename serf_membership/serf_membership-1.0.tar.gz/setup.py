#!/usr/bin/env python

from __future__ import with_statement
from serf_membership import version
import distutils.core
import os

# Importing setuptools adds some features like "setup.py develop", but
# it's optional so swallow the error if it's not there.
try:
    import setuptools
except ImportError:
    pass

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

distutils.core.setup(name='serf_membership',
      version=version,
      description='This is very simle script for election a leader (primary) from all members tagget with specific role.',
      author='Marian Ignev',
      author_email='m@ignev.net',
      url='https://github.com/mignev/serf-membership',
      packages=['serf_membership'],
      long_description=read('README.md'),
      install_requires = ['serfclient'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Operating System :: POSIX',
          'Operating System :: POSIX :: BSD',
          'Operating System :: POSIX :: Linux',
          'Operating System :: Unix',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Topic :: System :: Shells',
          'Topic :: Utilities',
          ],
     )
