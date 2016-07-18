import os
from setuptools import setup

# version (shape.function.path)
# python setup.py sdist upload
setup(
	name='django-autocomplete-x',
	version='0.0.6',
	packages=['django_autocomplete', ],
	url='https://github.com/exildev/django-autocomplete',
	author="Luis Miguel Morales Pajaro",
	author_email="luismiguel.mopa@gmail.com",
	licence="Creative Common",
	description="django autocomplete plugin",
	platform="Linux",
	zip_safe=False,
	include_package_data=True,
	package_data={'django_autocomplete': [
		'static/django_autocomplete/css/*.css',
		'static/django_autocomplete/js/*.js'
	]},
)