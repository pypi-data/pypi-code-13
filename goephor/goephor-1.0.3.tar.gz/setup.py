'''
Created on Apr 29, 2016

@author: iitow
'''
import json
import sys
from setuptools import setup, find_packages
SRCDIR = 'src'
def readme():
    ''' Spits out README.rst for our long_description
    with open('README.rst', 'r') as fobj:
        return fobj.read()
    '''
packages = ['requests',
            'PyYAML==3.10',
            'GitPython==2.0.2']

if sys.version_info < (2,7):
    packages.append('importlib')
    packages.append('argparse')

setup(
    name='goephor',
    version='1.0.3',
    description="A build automation tool to drive processes described in a yaml manifest. Supported on [Freebsd, Linux, OSX] systems",
    long_description=readme(),
    author='ian.itow',
    author_email='itow0001@gmail.com',
    url='https://github.com/itow0001/goephor',
    license='MIT',
    classifiers=[
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 2.7',
    ],
    package_dir={'': SRCDIR},
    package_data={'': ['*.json']},
    packages=find_packages(SRCDIR),
    zip_safe=False,
    install_requires=packages,
    entry_points={
        'console_scripts': ['goephor = goephor.__main__:main']
    },
    include_package_data=True,
)
