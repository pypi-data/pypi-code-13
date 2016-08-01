from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

__version__ = '1.0.1'

setup(
    name='unisquid',
    version=__version__,
    description='Yet another unittest extension for python.',
    long_description=long_description,
    url='https://github.com/beylsp/unisquid',
    download_url='https://github.com/beylsp/unisquid/tarball/' + __version__,
    license='MIT',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Programming Language :: Python',
      'Programming Language :: Python :: 2',
      'Programming Language :: Python :: 2.7',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.3',
      'Programming Language :: Python :: 3.4',
    ],
    packages=find_packages(),
    install_requires=['six'],
    keywords=['testing'],
    author='Patrik Beyls',
    test_suite = "tests",
)
