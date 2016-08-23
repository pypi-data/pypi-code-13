#!/usr/bin/env python

import os
from setuptools import setup, find_packages

setup(name = 'bam_reheader',
      author = 'Jeremiah H. Savage',
      author_email = 'jeremiahsavage@gmail.com',
      version = 0.25,
      description = 'reheader a BAM to include GDC @SQ info',
      url = 'https://github.com/jeremiahsavage/bam_reheader/',
      license = 'Apache 2.0',
      packages = find_packages(),
      install_requires = [
      ],
      classifiers = [
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ],
      data_files=[( '',['bam_reheader/GRCh38.d1.vd1.dict'])],
      entry_points={
          'console_scripts': ['bam_reheader=bam_reheader.__main__:main']
      },
)
