from setuptools import setup

setup(name='umls_request_manager',
	version='0.3',
	description='Authenticates, caches, and pipelines requests to the UMLS REST metathesaurus API',
	url='http://github.com/aduriseti/umls_request_manager',
	author='Amal Duriseti',
	author_email='aduriseti@gmail.com',
	license='MIT',
	packages=['umls_request_manager'],
	install_requires=[
		'requests',
		'grequests',
		'pyquery',
		'lxml',
	],
	zip_safe=False)
