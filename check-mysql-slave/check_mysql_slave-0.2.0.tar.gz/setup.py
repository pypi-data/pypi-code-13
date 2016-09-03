#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='check_mysql_slave',
      version=open('VERSION', 'r').read(),
      description='''Check MySQL seconds behind master for Nagios-like
    monitoring.''',
      long_description=open('README.rst', 'r').read(),
      url='https://www.shore.co.il/git/check_mysql_slave',
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
      keywords='nagios mysql slave replication monitoring',
      packages=find_packages(),
      install_requires=['MySQL-python'],
      entry_points={
          'console_scripts': [
              'check_mysql_slave=check_mysql_slave:main'
          ],
      }, )
