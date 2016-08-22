import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-multiimap',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='GPL',  
    description='A simple Django app to handle imap login.',
    long_description=README,
    url='',
    author='Infoporto',
    author_email='',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9',  
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',  
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
	'Programming Language :: Python :: 2.7',
	'Programming Language :: Python :: 3.2',
	'Programming Language :: Python :: 3.3',
	'Programming Language :: Python :: 3.4',
	'Programming Language :: Python :: 3.5'
    ],
) 
