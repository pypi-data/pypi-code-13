#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.md') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.md') as history_file:
    history = history_file.read()

requirements = [
    'Pillow',
]

setup(
    name="img-percent-diff",
    version='0.1.0',
    description="Calculates the percent area that two images differ",
    long_description=readme + '\n\n' + history,
    author="Mike Charles",
    author_email='mike.charles@noaa.gov',
    url="https://github.com/cpc/img-percent-diff",
    packages=[
        'img_percent_diff',
    ],
    package_dir={'img_percent_diff':
                 'img_percent_diff'},
    include_package_data=True,
    install_requires=requirements,
    license="CC",
    zip_safe=False,
    keywords='img-percent-diff',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
    ],
    entry_points={
        'console_scripts': [
            "img-percent-diff = img_percent_diff:main"
        ]
    },
)
