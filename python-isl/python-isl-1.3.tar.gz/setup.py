import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='python-isl',
    version='1.3',
    author='Joseph Solomon',
    author_email='josephs@isl.co',
    description=('A python package to wrap the islapi.'),
    license='MIT',
    keywords='python isl api',
    url='https://github.com/istrategylabs/python-isl',
    packages=['pythonisl', ],
    long_description=read('README'),
    classifiers=[
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=['requests>=2.10,<2.11', 'PyJWT>=0.4,<0.5'],
)
