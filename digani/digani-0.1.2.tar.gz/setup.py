from distutils.core import setup
from setuptools import Extension,find_packages
from os import path

setup(
    name = 'digani',
    version = '0.1.2',
    description = 'automatically identify column names',
    author = 'Lingzhe Teng',
    author_email = 'zwein27@gmail.com',
    url = 'https://github.com/ZwEin27/dig-attribute-name-identification',
    download_url = 'https://github.com/ZwEin27/dig-attribute-name-identification/tarball/0.1.2',
    packages = find_packages(),
    package_data={'': ['*.json']},
    # scripts=['run-digani'],
    keywords = ['dig', 'name', 'identify', 'attribute', 'column'],
    install_requires=['pnmatcher', 'pygtrie', 'digpe', 'inflection', 'nose2', 'phonenumbers', 'python-dateutil', 'six', 'wsgiref']
)