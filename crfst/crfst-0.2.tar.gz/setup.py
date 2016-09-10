import os

from setuptools import setup, find_packages

__author__ = 'Aleksandar Savkov'


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='crfst',
    version='0.2',
    description='A multi-purpose sequential tagger wrapped around CRFSuite',
    author='Aleksandar Savkov',
    author_email='aleksandar@savkov.eu',
    url='https://github.com/savkov/CRFSuiteTagger',
    packages=find_packages(),
    install_requires=['numpy', 'bioeval', 'python-crfsuite'],
    license='GPLv3',
    long_description=read('README.md'),
    keywords='CRF CRFSuite sequence tagging POS chunking NER',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    platforms=['Unix', 'MacOS']
)
