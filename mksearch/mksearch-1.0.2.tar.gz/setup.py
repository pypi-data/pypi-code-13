'''
Created on Apr 29, 2016

@author: iitow
'''
from setuptools import setup, find_packages

SRCDIR = 'src'

def readme():
    ''' 
    Do you need to easily relate a C source code change check-in to a binary?
    This tool recursively grabs all the Makefiles parses each file and if a value
    is found produces a json file containing the relevant info.
    Currently supports:
    - Variables
    - Includes
    - Comments
    The goal is to fully support GNU make standards:
    https://www.gnu.org/software/make/manual/html_node/Quick-Reference.html
    
    This tools was designed to support Freebsd but should work for all systems 
    using GNU make
    '''
setup(
    name='mksearch',
    version='1.0.2',
    description="Recursively search makefiles for a value and output json parseable list",
    long_description=readme(),
    author='Ian Itow',
    author_email='itow0001@gmail.com',
    url='https://github.com/itow0001/mksearch',
    license='MIT',
    classifiers=[
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 2.7',
    ],
    package_dir={'': SRCDIR},
    packages=find_packages(SRCDIR),
    zip_safe=False,
    install_requires=[
    ],
    entry_points={
        'console_scripts': ['mksearch = makefile_parser.__main__:main']
    },
    include_package_data=True,
)