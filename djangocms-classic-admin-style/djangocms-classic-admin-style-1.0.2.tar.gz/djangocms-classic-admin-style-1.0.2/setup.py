import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name='djangocms-classic-admin-style',
    version='1.0.2',
    license='MIT License',
    description='Enables Django\'s original admin styling to work nicely with Django CMS',
    long_description=README,
    url='https://github.com/tdsymonds/djangocms-classic-admin-style',
    author='Tom Symonds',
    author_email='tdsymonds@hotmail.com',
    keywords='djangocms-classic-admin-style, django, cms, admin, style',
    packages=[
        'djangocms_classic_admin_style',
    ],
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
