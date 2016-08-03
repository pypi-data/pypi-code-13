#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = ['six==1.10.0', 'pycrypto==2.6.1']
test_requirements = ['pytest-cov==2.3.0']
setup_requirements = ['pytest-runner==2.9']

setup(
    name='dirigible',
    version='0.2.7',
    description="Config encryption",
    long_description=readme,
    author="Thom Neale",
    author_email='tneale@massmutual.com',
    url='https://github.org/massmutual/dirigible',
    packages=find_packages(),
    package_dir={'dirigible': 'dirigible'},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='dirigible',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
