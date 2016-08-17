from distutils.core import setup

setup(
	name = 'relog',
	version = '1.0',
	description = 'Wrap logging round 3rd party functions and calls',
	author = 'Jesters Ghost',
	author_email = 'jestersghost@gmail.com',
	url = 'https://bitbucket.org/jestersghost/relog',
	package_dir = { 'relog': '.' },
	packages = [
		'relog',
	],
)
