#!/usr/bin/env python
"""yqmq build & installation script"""

from setuptools import setup


install_requires = ['gevent']
setup_requires = []

setup(name='yqmq',
      version='0.0.5',
      description='YQMQ Python AMQP Client Library With Gevent Support',
      keywords = ['amqp', 'gevent', 'rabbitmq'],
      maintainer='Wu Wenchao',
      maintainer_email='cainbit@gmail.com',
      url='https://github.com/cainbit/yqmq',
      packages=['yqmq'],
      license='MIT',
      install_requires=install_requires,
      setup_requires=setup_requires,
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.7',
          'Topic :: Communications',
          'Topic :: Internet',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: System :: Networking'],
      zip_safe=True
)
