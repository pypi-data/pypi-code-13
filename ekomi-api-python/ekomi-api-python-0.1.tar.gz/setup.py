# coding=utf-8
"""
ekimo API setup
"""
__copyright__ = 'Copyright 2016, DNest'

from setuptools import setup, find_packages

# Dynamically calculate the version based on ekomi.VERSION.
VERSION = __import__('ekomi').get_version()


setup(
    name='ekomi-api-python',
    version=VERSION,
    url='https://bitbucket.org/abalt/ekomi-api-python',
    author='DNest',
    author_email='admin@dnestagency.com',
    description=(
        "This package connect to EKOMI API."),
    long_description=open('README.rst').read(),
    keywords="ekomi, order, reviews",
    license=open('LICENSE').read(),
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests'
    ],
    download_url='https://bitbucket.org/abalt/ekomi-api-python/get/0.1.0.zip',
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
