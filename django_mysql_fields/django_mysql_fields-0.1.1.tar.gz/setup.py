import os
from setuptools import find_packages, setup


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

setup(
    name='django_mysql_fields',
    version='0.1.1',
    packages=find_packages(),
    license='BSD License',
    description='Useful Django fields for use with MySQL.',
    long_description=README,
    url='https://github.com/multiplay/django-mysql-fields',
    author='Multiplay UK Ltd',
    author_email='support@multiplay.co.uk',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)
