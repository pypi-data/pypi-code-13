from setuptools import setup

setup(name='umls_request_manager',
	version='0.2',
	description='Authenticates, caches, and pipelines requests to the UMLS REST metathesaurus API',
	url='http://github.com/aduriseti/umls_request_manager',
	author='Amal Duriseti',
	author_email='aduriseti@gmail.com',
	license='MIT',
	packages=['umls_request_manager'],
	install_requires=[
		'requests',
		'grequests',
		'signal',
		'sys',
		'time',
		'json',
		'pickle',
		'shelve',
		'copy',
	],
	zip_safe=False)
