import os
import sys

from setuptools import find_packages, setup


setup(
    name='django-simple-quiz',
    version='0.1.1',
    author="Mike Dingjan",
    author_email='mike@mikedingjan.nl',
    url='',
    description='Django Quiz App',
    long_description=open('README.md').read(),
    keywords='django, quiz',
    platforms=['osx', 'linux'],
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        'django-formtools==1.0',
        'django-model-utils==2.5.2',
        'Pillow==3.3.1',
    ],
    include_package_data=True,
    license='Apache License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],
)
