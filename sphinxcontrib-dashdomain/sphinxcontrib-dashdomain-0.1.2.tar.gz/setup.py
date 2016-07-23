# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = '''
This package contains the dash domain and builder Sphinx extension.
This extension provides a dash domain for sphinx
'''

requires = ['Sphinx>=1.4']

setup(
    name='sphinxcontrib-dashdomain',
    version='0.1.2',
    url='http://bitbucket.org/togakushi/sphinxcontrib-dashdomain',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-dashdomain',
    license='BSD',
    author='@togakushi',
    author_email='nina.togakushi at gmail dot com',
    description='Sphinx "dash domain" and "builder" extension',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Sphinx :: Extension',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['sphinxcontrib'],
)
