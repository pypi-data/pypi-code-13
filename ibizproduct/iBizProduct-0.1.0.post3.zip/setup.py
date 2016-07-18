from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='iBizProduct',

    version='0.1.0',

    description='iBizProduct library for python products',
    long_description=long_description,

    url='https://code.ibizservices.com/lrivera/iBizProduct-Python',

    author='Luis Rivera',
    author_email='lrivera@xelaweb.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='library iBizAPI development',

    packages=find_packages(),

    install_requires=['requests', 'future'],
)