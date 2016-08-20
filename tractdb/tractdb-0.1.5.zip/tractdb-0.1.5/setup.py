# This file compiled from setup.py.in
import setuptools

VERSION = '0.1.5'

setuptools.setup(
    name='tractdb',
    version=VERSION,
    description='TractDB',
    url='https://tractdb.org',
    packages=['tractdb'],
    install_requires=[
        'couchdb',
        'pyyaml',
    ],
    entry_points={
        'console_scripts': [],
    },
    zip_safe=False,
)
