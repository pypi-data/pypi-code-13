#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name = 'picard_tool',
      author = 'Jeremiah H. Savage',
      author_email = 'jeremiahsavage@gmail.com',
      version = 0.107,
      description = 'call picard tools and store time/mem metrics in sqlitedb',
      url = 'https://github.com/jeremiahsavage/picard_tool',
      license = 'Apache 2.0',
      packages = find_packages(),
      install_requires = [
          'pandas',
          'sqlalchemy',
          'cdis_pipe_utils'
      ],
      classifiers = [
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ],
)
