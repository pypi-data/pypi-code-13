from setuptools import setup

setup(
	name='QualiCSCLI',
	version='0.1',
	py_modules=['QualiCSCLI'],
	install_requires=['requests',],
	entry_points='''
		[console_scripts]
		QualiCSCLI=QualiCSCLI:cli
	''',
)
