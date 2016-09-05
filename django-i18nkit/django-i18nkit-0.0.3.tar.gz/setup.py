#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django-i18nkit',
    version='0.0.3',
    author='Aarni Koskela',
    author_email='akx@iki.fi',
    description='Internationalization utilities for Django.',
    license='MIT',
    packages=find_packages(exclude=["test*"]),
    zip_safe=False,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    install_requires=[
        'babel<3.0',
        'Django>=1.8,<1.10',
        'django_babel>=0.5.0',
    ]
)
