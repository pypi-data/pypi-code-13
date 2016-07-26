import os
import sys
from setuptools import setup, find_packages

# Some initialization
here = os.path.abspath(os.path.dirname(__file__))
long_description = open(os.path.join(here, 'README.md')).read()


data_files = []
root_dir = os.path.dirname(__file__)
if root_dir:
	os.chdir(root_dir)


# this code snippet is taken from django-registration setup.py script
for dirpath, dirnames, filenames in os.walk('jalali_date'):
	# Ignore dirnames that start with '.'
	for i, dirname in enumerate(dirnames):
		if dirname.startswith('.'):
			del dirnames[i]
	if filenames:
		prefix = dirpath[13:] # Strip "jalali_date/" or "jalali_date\"
		for f in filenames:
			data_files.append(os.path.join(prefix, f))	

setup(
        name='django-jalali-date',
        version='0.1.8',
        packages=find_packages(),
        description = ('Jalali Date support for user interface. Easy conversion of DateTimeFiled to JalaliDateTimeField within the admin site.'),
        url = 'http://github.com/a-roomana/django-jalali-date',
        download_url = 'https://pypi.python.org/pypi/django-jalali-date/',
        author = 'Arman Roomana',
        author_email = 'roomana.arman@gmail.com',
        keywords = "django jalali date",
        license='Python Software Foundation License',
        platforms='any',
        requires = ["jdatetime","django"],
        long_description=long_description,
	package_dir={'jalali_date': 'jalali_date'},
    	package_data={'jalali_date': data_files},
	zip_safe=False,
)
