"""Standard setuptools.
"""
from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

README = path.join(here, 'README.txt')

if path.isfile(README):
    with open(README) as f:
        long_description = f.read()
else:
    long_description = ''

setup(
    name='django-madcap-flare',
    version='0.0.1',

    description='Integrate Madcap Flare docs into your Django project',
    long_description=long_description,
    url='https://github.com/mypebble/django-madcap-flare',
    author='Pebble',
    author_email='scott.walton@mypebble.co.uk',
    license='MIT',
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='django madcap flare web development',
    packages=['madcap_flare'],
    install_requires=['django'],
    extras_require={
        'dev': [],
        'test': [],
    },
)
