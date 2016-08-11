"""
    a simple version of the setup() command from:
    https://setuptools.readthedocs.io/en/latest/setuptools.html
"""
from setuptools import setup, find_packages
from codecs import open
from os import path

# Get the long description from the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    # name is the handle you use to import this package.
    name="HydroFunctions",
    version="0.0.0",
    description='convenience functions for hydrology',
    long_description=long_description,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Utilities'
    ],
    keywords='',
    url='https://github.com/mroberge/hf',
    author='Martin Roberge',
    author_email='mroberge.whois@gmail.com',
    license='MIT',
    # packages=['roberge_sample'],
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas'
    ],
    test_suite='nose2.collector.collector',
    # I guess you don't need to install unittest since it is part of the main
    # tests_require=['unittest'],
    include_package_data=True,
    zip_safe=False,
)
