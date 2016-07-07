"""Python setuptools build script."""

import setuptools


__version__ = '0.1.0'


setuptools.setup(
    name='kube',
    version=__version__,
    author='Floris Bruynooghe',
    author_email='flub@cobe.io',
    license='LGPLv3',
    url='http://bitbucket.org/cobeio/kube',
    description='Pythonic Kubernetes API',
    packages=setuptools.find_packages(),
)
