from setuptools import setup, find_packages

setup(
	name='QualiCSCLI',
	version='0.4',
	py_modules=['QualiCSCLI'],
	packages=find_packages(),
	install_requires=['requests',],
	entry_points='''
		[console_scripts]
		QualiCSCLI=QualiCSCLI:cli
	''',
)
