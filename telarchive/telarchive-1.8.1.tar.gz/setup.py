# Always prefer setuptools over distutils
from setuptools import setup, find_packages

setup(name="telarchive",
	version="1.8.1",
	# [ ] description
	# [ ] long_description
	url="http://www.mpe.mpg.de/~erwin/code/",
	author="Peter Erwin",
	author_email="erwin@mpe.mpg.de",
	license="GPL",

	classifiers=[
		# How mature is this project?
		"Development Status :: 5 - Production/Stable",
		
		# [ ] Intended audience
		
		# [ ] License
		
		# Specify supported Python versions
		"Programming Language :: Python :: 2",
		"Programming Language :: Python :: 2.6",
		"Programming Language :: Python :: 2.7",
	],
	
	# [ ] keywords
	packages=['telarchive'],
	scripts=['dosearch.py', 'do_fetchsdss.py', 'do_fetchsdss_spectra.py']
	)
	
