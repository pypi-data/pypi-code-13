#!/usr/bin/env python

from setuptools import find_packages, setup


setup(
    name='django-mptt-nomagic',
    description='''Utilities for implementing Modified Preorder Tree Traversal
        with your Django Models and working with trees of Model instances.''',
    version=__import__('mptt').__version__,
    author='Matthias Kestenholz',
    author_email='mk@feinheit.ch',
    url='https://github.com/matthiask/django-mptt/tree/mk/nomagic',
    license='MIT License',
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        'Topic :: Utilities',
    ],
)
