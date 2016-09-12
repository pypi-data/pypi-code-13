from setuptools import setup

setup(
	name='colorecho',
	version='0.2',
	description='Wrap your strings in terminal color codes. From a terminal command.',
	url='https://github.com/mahyar/colorecho',
	author='Mahyar McDonald',
	author_email='no.email@example.com',
	license='MIT',
	packages=['colorecho'],
	scripts=['bin/colorecho'],
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Environment :: Console',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 2',
	]
)
