#!/usr/bin/python2

from setuptools import setup, find_packages
setup(name='py-cassandra-journal-forwarder',
      version='0.6',
      author='Max Chesterfield',
      license='MIT',
      description='Forwards systemd journal to a cassandra cluster',
      packages=find_packages())
