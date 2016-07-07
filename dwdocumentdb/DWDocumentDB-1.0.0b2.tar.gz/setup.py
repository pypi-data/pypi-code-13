from setuptools import setup, find_packages
from codecs import open
from os import path

here=path.abspath(path.dirname(__file__))

#get the long description from the README file 
with open(path.join(here,'README.md'),encoding='utf-8') as f:
	long_description=f.read()

setup(
	name='DWDocumentDB',
	version='1.0.0b2',
	description='Python library wrapper for pydocumentdb',
	long_description=long_description,
	url='https://github.com/kurniawano/DWDocumentDB',
	author='Oka Kurniawan',
	author_email='kurniawano@ieee.org',
	license='MIT',
	classifiers=[
	'Development Status :: 4 - Beta',
	'Intended Audience :: Education',
	'License :: OSI Approved :: MIT License',
	'Programming Language :: Python :: 2.7'
	],
	keywords='documentdb microsoft api wrapper',
	packages=find_packages(exclude=['contrib','docs','tests']),
	install_requires=['pydocumentdb'],
	
	)