# Imports from python.  # NOQA
from setuptools import setup, find_packages  # NOQA
import os


DESCRIPTION = 'A lightweight plugin for managing Django formsets with jQuery.'

REPO_URL = 'https://github.com/dallasmorningnews/django-dynamic-formsets'

VERSION = '0.0.8'


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='django-dynamic-formsets',
    version=VERSION,
    description=DESCRIPTION,
    long_description=read('README.md'),
    url=REPO_URL,
    download_url=REPO_URL + '/tarball/' + VERSION,
    author='Allan James Vestal, The Dallas Morning News',
    author_email='ajvestal@dallasnews.com',
    license='BSD',
    packages=find_packages(exclude=['demo']),
    include_package_data=True,
    keywords=['django', 'formset', 'javascript'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.1',
        # 'Programming Language :: Python :: 3.2',
        # 'Programming Language :: Python :: 3.3',
    ],
    zip_safe=False,
)
