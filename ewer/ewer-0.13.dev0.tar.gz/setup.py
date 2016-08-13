#!/usr/bin/env python

import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.version_info < (3, 5):
    raise NotImplementedError("Sorry, you need at leastPython 3.5+ to use ewer.")

import bottle

setup(name='ewer',
      version=bottle.__version__,
      description='Async Fork of Fast and simple WSGI-framework for small web-applications.',
      long_description=bottle.__doc__,
      author=bottle.__author__,
      author_email='sam@ioflo.com',
      url='http://ioflo.com',
      py_modules=['ewer'],
      scripts=[],
      license='MIT',
      platforms='any',
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
                   'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
                   'Topic :: Internet :: WWW/HTTP :: WSGI',
                   'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
                   'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
                   'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
                   'Topic :: Software Development :: Libraries :: Application Frameworks',
                   'Programming Language :: Python :: 3.5',
                   ],
      )
