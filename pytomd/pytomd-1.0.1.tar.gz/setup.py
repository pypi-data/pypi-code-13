'''
Created on Apr 29, 2016

@author: iitow
'''
from setuptools import setup, find_packages

SRCDIR = 'src'


def readme():
    ''' Spits out README.rst for our long_description
    with open('README.rst', 'r') as fobj:
        return fobj.read()
    '''


setup(
    name='pytomd',
    version='1.0.1',
    description="Easy python project document generator to github README.md file",
    long_description=readme(),
    author='Ian Itow',
    author_email='itow0001@gmail.com',
    url='https://github.com/itow0001/pytomd',
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
        'console_scripts': ['pytomd = pytomd.__main__:main']
    },
    include_package_data=True,
)