import os
from setuptools import setup, find_packages

__version__ = '1.0.3'


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='maptiler',
    version=__version__,
    author='Nils Ziehn',
    author_email='nziehn@gmail.com',
    url='https://github.com/nziehn/maptiler',
    description='Allows custom geohash bucket sizes and finding buckets in vicinity of given location',
    long_description=read('README.md'),
    license='MIT',
    keywords='python geohash tiles',
    download_url='https://github.com/nziehn/maptiler/archive/{version}.tar.gz'.format(version=__version__),
    packages=find_packages(),
)