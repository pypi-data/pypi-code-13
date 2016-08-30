import os
import sys

from setuptools import setup, find_packages

setup(name='gym_vnc',
      version='0.0.7',
      packages=[package for package in find_packages()
                if package.startswith('gym_vnc')],
      install_requires=['gym>=0.2.3', 'docker-py', 'Pillow', 'autobahn', 'twisted', 'ujson',
                        # Not actually needed, but Twisted will print
                        # scary warnings unless it's installed
                        'service_identity'
      ],
      extras_require={
          'atari': 'gym[atari]',
          # Faster vnc driver
          'go': ['go-vncdriver'],
      }
)
