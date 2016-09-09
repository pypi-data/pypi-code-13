#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name='django-i18nkit',
    version='0.0.5',
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
        'Django>=1.8',
    ],
    entry_points={
        'babel.extractors': [
            'ik_django = i18nkit.django_extract:django_extract',
            'ik_jinja2 = i18nkit.jinja2_extract:jinja2_extract',
        ],
    },
)
