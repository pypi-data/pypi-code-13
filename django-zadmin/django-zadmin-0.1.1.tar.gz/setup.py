from __future__ import unicode_literals
import os
from setuptools import find_packages, setup


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name='django-zadmin',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='another admin template for django with bootstrap4.0 and sass.',
    long_description=README,
    url='http://zadmin.zhaowentao.cn/',
    author='steven zhao',
    author_email='wentao79@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)
