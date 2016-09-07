from setuptools import setup

setup(
	name="mdrs",
	version="0.0.1",
	packages=["mdrs",],
	license="",
	long_description="docker images manager",
	entry_points = {
		'console_scripts':[
			'mdrs = mdrs:main'
		],
	}
)
