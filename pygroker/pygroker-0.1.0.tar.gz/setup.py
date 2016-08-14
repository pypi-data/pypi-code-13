from setuptools import setup
import os

long_desc = ''

if os.path.exists('README.rst'):
    long_desc = open('README.rst').read()

setup(name = 'pygroker',
    version = '0.1.0',
    description = 'Temporary package for https://github.com/garyelephant/pygrok/pull/3',
    long_description= long_desc,
    url = 'https://github.com/garyelephant/pygrok',
    author = 'garyelephant',
    author_email = 'garygaowork@gmail.com',
    license = 'MIT',
    packages = ['pygrok'],
    include_package_data = True,
    keywords = ['python grok', 'regex'], # arbitrary keywords
    download_url = 'https://github.com/garyelephant/pygrok/tarball/v0.7.4',
    install_requires=['regex']
    )
