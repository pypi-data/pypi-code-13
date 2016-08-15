#!/usr/bin/env python

from distutils.core import setup

setup(name='pyzmq-wrapper',
	  version='0.2.1',
	  description='Wrapper classes for pyzmq',
	  long_description='Please visit https://github.com/supercoderz/pyzmq-wrapper for more details',
	  author='Narahari Allamraju',
	  author_email='anarahari@gmail.com',
	  url='https://github.com/supercoderz/pyzmq-wrapper',
	  packages=['zmqwrapper'],
	  install_requires=['pyzmq','pytest'],
	classifiers = [
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3',
	]
	 )
