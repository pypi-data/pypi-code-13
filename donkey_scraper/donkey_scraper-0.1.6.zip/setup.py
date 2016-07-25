import setuptools
from distutils.core import setup


setup(
	name = 'donkey_scraper',
	version = '0.1.6',
	description = 'A Simple web scraper',
	author = 'Gregory Roberts',
	author_email = 'greg.roberts1991@gmail.com',
	url = 'https://github.com/gregroberts/Donkey',
	download_url = 'https://github.com/gregroberts/Donkey',
	keywords = ['scraping','web'],
	classifiers = [],
	packages = ['donkey'],
	install_requires = [
		'jmespath',
		'lxml',
	]
)