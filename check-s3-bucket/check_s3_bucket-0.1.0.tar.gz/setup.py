#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='check_s3_bucket',
      version=open('VERSION', 'r').read(),
      description='''Check that a filename matching the regex was added to the
    bucket in the given time window.''',
      long_description=open('README.rst', 'r').read(),
      url='https://www.shore.co.il/git/check_s3_bucket',
      author='Nimrod Adar',
      author_email='nimrod@shore.co.il',
      license='MIT',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: System Administrators',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 2', 'Topic :: Utilities',
          'License :: OSI Approved :: MIT License'
      ],
      keywords='nagios s3 aws monitoring',
      packages=find_packages(),
      install_requires=['python-dateutil', 'botocore'],
      entry_points={
          'console_scripts': [
              'check_s3_bucket=check_s3_bucket:main'
          ],
      }, )
