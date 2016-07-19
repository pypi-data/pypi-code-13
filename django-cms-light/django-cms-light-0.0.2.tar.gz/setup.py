from setuptools import setup, find_packages, Command
import os, sys


setup(
    name='django-cms-light',
    version='0.0.2',
    description='Django CMS Light provides internet as a service for your friends.',
    author='Django CMS Light Pic',
    author_email='jpic@yourlabs.org',
    url='http://dcl-cms.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    license = 'MIT',
    install_requires=[
        'psycopg2',
        'django-pages-cms',
    ],
    entry_points = {
        'console_scripts': [
            'dcl = dcl.manage:main',
        ],
    },
    classifiers = [
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
