#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name = 'cdis_pipe_utils',
      author = 'Jeremiah H. Savage',
      author_email = 'jeremiahsavage@gmail.com',
      version = 0.19,
      description = 'Reusable code to call pipeline tools and get time/mem metrics',
      url = 'https://github.com/LabAdvComp/cdis_pipe_utils',
      license = 'Apache 2.0',
      packages = find_packages(),
      install_requires = [
          'pandas',
          'psycopg2>=2.6.1',
          'sqlalchemy'
      ],
      classifiers = [
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development :: Libraries',
      ],
)
