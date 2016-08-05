#!/usr/bin/python2

from setuptools import setup
setup(name='py-cassandra-journal-forwarder',
      version='0.3',
      author='Max Chesterfield',
      license='MIT',
      description='Forwards systemd journal to a cassandra cluster',
      py_modules=['cassandra-journal-forwarder'])
