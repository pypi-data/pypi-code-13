from setuptools import setup

try:
	with open("README.md") as f:
		for i, line in enumerate(f):
			if i == 1:
				desc = line
			elif i > 1:
				break
except FileNotFoundError:
	pass


setup(name='kaczmarz',
	version='5',
	description=desc,
	url='https://github.com/lightningleaf/kaczmarz',
	author='lightningleaf',
	author_email='lightningleaf0@gmail.com',
	license='None',
	packages=['kaczmarz'],
	install_requires=[
	'recordclass',
	],
	zip_safe=False,
	classifiers=[
	'Programming Language :: Python :: 3.5',
	]
	)