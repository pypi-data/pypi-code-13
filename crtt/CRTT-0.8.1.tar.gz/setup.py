#!/usr/bin/env python3
from distutils.core import setup
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
	long_description = f.read()

setup(name='CRTT',
	version='0.8.1',
	description='Common Restful Test Tool',
	long_description= long_description,
	author='Trelay Wang',
	author_email='trelwan@celestica.com',
	url='https://github.com/trelay/CRTT',
	license='MIT',
	classifiers=[
		# How mature is this project? Common values are
		#   3 - Alpha
		#   4 - Beta
		#   5 - Production/Stable
		'Development Status :: 4 - Beta',

		# Indicate who your project is intended for
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',

		# Pick your license as you wish (should match "license" above)
		'License :: OSI Approved :: MIT License',

		# Specify the Python versions you support here. In particular, ensure
		# that you indicate whether you support Python 2, Python 3 or both.
		'Programming Language :: Python :: 3',
    ],
	keywords='restful test tool',
	packages=['CRTT'],
	package_data={'CRTT':['test/*.conf','test/*.py']},
	download_url='https://github.com/trelay/CRTT/tarball/0.8.1',
)
