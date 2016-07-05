# coding=utf-8
"""
Idealista API setup
"""
__copyright__ = 'Copyright 2016, DNest'

from setuptools import setup, find_packages

# Dynamically calculate the version based on idealista.VERSION.
VERSION = __import__('idealista').get_version()


setup(
    name='idealista-api-python',
    version=VERSION,
    url='https://bitbucket.org/abalt/idealista-api-python',
    author='DNest',
    author_email='admin@dnestagency.com',
    description=(
        "Upload properties to Idealista using IDEALISTA API."),
    long_description=open('README.rst').read(),
    keywords="Idealista, Properties, Rent, Sale",
    license=open('LICENSE').read(),
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    download_url='https://bitbucket.org/abalt/idealista-api-python/get/0.1.1.zip',
    # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Other/Nonlisted Topic'],
)
