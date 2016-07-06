from setuptools import setup, find_packages, Command

from codecs import open
from os import path

version = "0.0.1"
short_description = "Ordered value getter from Dictionary type value."
here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
#     requires = f.readlines()

setup(
    name='OrderedFormat',
    version=version,
    description=short_description,
    long_description=long_description,
    url='https://github.com/Himenon/OrderedFormat',
    author='K.Himeno',
    author_email='k.himeno314@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='ordered dictionary',
    packages=find_packages(exclude=['tests']),
    install_requires=["pyyaml", "yamlordereddictloader", "six"],
    tests_require=["nose"],
)