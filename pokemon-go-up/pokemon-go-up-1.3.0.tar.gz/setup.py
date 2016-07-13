from distutils.core import setup
from setuptools import find_packages

setup(
    name='pokemon-go-up',
    version='1.3.0',
    scripts=['pokemon-go-up'],
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='Python tools to check pokemon go server status',
    long_description='Python tools to check pokemon go server status',
    install_requires=['requests'],
    url='http://github.com/ariestiyansyah/pokemon-go-up',
    author='Rizky Ariestiyansyah',
    author_email='ariestiyansyah.rizky@gmail.com'
)
