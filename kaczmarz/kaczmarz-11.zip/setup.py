from setuptools import setup

try:
	with open("README.md") as rdmf:
		for i, line in enumerate(rdmf):
			if i == 1:
				desc = line
			elif i > 1:
				break
except FileNotFoundError:
	desc = 'Simulations and visualizations of the Kaczmarz algorithm on various classifications of linear systems'
	pass

setup(name='kaczmarz',
	version='11',
	description=desc,
	url='https://github.com/lightningleaf/kaczmarz',
	author='lightningleaf',
	author_email='lightningleaf0@gmail.com',
	license='None',
	packages=['kaczmarz'],
	install_requires=[
	'recordclass',
	'numpy'
	],
	zip_safe=False,
	classifiers=[
	'Programming Language :: Python :: 3.5',
	]
	)