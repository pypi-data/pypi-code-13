#!/usr/bin/env python

from distutils.core import setup

setup(name='sensu-auditor',
      version='0.0.1.1',
      description='Parse through sensu logs and upload to elasticsearch',
      author='Ben Waters',
      author_email='ben@book-md.com',
      install_requires=['elasticsearch', 'python-dateutil', 'configparser'],
      packages=['sensu_auditor'],
      scripts=['bin/sensu-auditor'],
      url="https://github.com/bookmd/sensu-auditor",
      data_files=[('/etc/default/', ['configs/sensu-auditor.ini'])],
      )
