#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name = 'decider_bwa_se',
      author = 'Jeremiah H. Savage',
      author_email = 'jeremiahsavage@gmail.com',
      version = 0.5,
      description = 'match readgroup and fastq outputs',
      url = 'https://github.com/jeremiahsavage/decider_bwa_se',
      license = 'Apache 2.0',
      packages = find_packages(),
      install_requires = [
          'cython',
          'pandas',
          'biopython',
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
