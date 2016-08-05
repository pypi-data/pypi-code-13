#!/usr/bin/python2

from setuptools import setup, find_packages
setup(name='py-cassandra-journal-forwarder',
      version='0.9.1',
      author='Max Chesterfield',
      license='MIT',
      description='Forwards systemd journal to a cassandra cluster',
      packages=find_packages(),
      install_requires=['cassandra-driver', 'python-systemd'],
      include_package_data=True)

