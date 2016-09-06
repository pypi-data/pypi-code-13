from distutils.core import setup
from setuptools import find_packages


setup(
    name='talka2z',
    version='0.5',
    packages=find_packages(exclude=('tests', 'tests.*')),
    install_requires=[
    ]
)
