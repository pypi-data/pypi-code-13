from setuptools import setup

setup(name='kaczmarz',
	version='14',
	description='Simulations and visualizations of the Kaczmarz algorithm on various classifications of linear systems',
	url='https://github.com/lightningleaf/kaczmarz',
	author='lightningleaf',
	author_email='lightningleaf0@gmail.com',
	license='None',
	packages=['kaczmarz'],
	install_requires=[
	'recordclass',
	'numpy'
	],
	zip_safe=True,
	classifiers=[
	'Programming Language :: Python :: 3.5',
	'Intended Audience :: Science/Research'
	]
	)