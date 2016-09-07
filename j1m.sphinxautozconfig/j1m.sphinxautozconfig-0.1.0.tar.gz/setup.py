name, version = 'j1m.sphinxautozconfig', '0.1.0'

install_requires = ['setuptools', 'docutils']

from setuptools import setup

long_description=open('README.rst').read()

setup(
    author = 'Jim Fulton',
    author_email = 'jim@jimfulton.info',
    license = 'MIT',

    name = name, version = version,
    long_description = long_description,
    description = long_description.strip().split('\n')[1],
    packages = [name.split('.')[0]],
    namespace_packages = [name.split('.')[0]],
    package_dir = {'': 'src'},
    install_requires = install_requires,
    )
