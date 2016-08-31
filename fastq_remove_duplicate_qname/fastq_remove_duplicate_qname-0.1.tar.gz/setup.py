#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name = 'fastq_remove_duplicate_qname',
      author = 'Jeremiah H. Savage',
      author_email = 'jeremiahsavage@gmail.com',
      version = 0.1,
      description = 'remove duplicate QNAME from a fastq',
      url = 'https://github.com/jeremiahsavage/fastq_remove_duplicate_qname/',
      license = 'Apache 2.0',
      packages = find_packages(),
      install_requires = [
          'biopython == 1.68'
      ],
      classifiers = [
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ],
      entry_points={
          'console_scripts': ['fastq_remove_duplicate_qname=fastq_remove_duplicate_qname.__main__:main']
      }
)
