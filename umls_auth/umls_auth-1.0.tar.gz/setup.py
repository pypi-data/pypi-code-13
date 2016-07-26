from setuptools import setup

setup(name='umls_auth',
	version='1.0',
	description='Standalone authentication package for UMLS REST metathesaurus API',
	url='http://github.com/aduriseti/umls_auth',
	author='Amal Duriseti',
	author_email='aduriseti@gmail.com',
	license='MIT',
	packages=['umls_auth'],
	install_requires=[
		'requests',
		'pyquery',
		'lxml',
	],
	zip_safe=False)
