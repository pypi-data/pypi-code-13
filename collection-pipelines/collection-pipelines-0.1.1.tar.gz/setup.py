from setuptools import setup
from pip.req import parse_requirements


required_packages = [str(ir.req) for ir in \
    parse_requirements('requirements/prod.txt', session=False)]

setup(
    name='collection-pipelines',
    version='0.1.1',
    description='Framework to implement collection pipelines in python.',
    long_description=open('README.rst').read(),
    url='https://github.com/povilasb/pycollection-pipelines',
    author='Povilas Balciunas',
    author_email='balciunas90@gmail.com',
    license='MIT',
    packages=['collection_pipelines'],
    install_requires=required_packages,
)
