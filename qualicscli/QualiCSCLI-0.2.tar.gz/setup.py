from setuptools import setup

setup(
	name='QualiCSCLI',
	version='0.2',
	py_modules=['QualiCSCLI','Table'],
	install_requires=['requests',],
	entry_points='''
		[console_scripts]
		QualiCSCLI=QualiCSCLI:cli
	''',
)
