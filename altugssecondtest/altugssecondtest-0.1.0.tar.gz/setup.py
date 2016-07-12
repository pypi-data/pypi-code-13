from distutils.core import setup
from setuptools import find_packages
from distutils.core import Extension
#from setuptools import setup, find_packages
setup(
    name = 'altugssecondtest',
    packages = find_packages(),
    version = '0.1.0',
    description = 'A Python package example',
    author = 'altugb',
    author_email = 'altug.bitlislioglu@epfl.ch',
    url = 'https://altugb@bitbucket.org/altugb/altugssecondtest.git',    
    py_modules=['altugssecondtest'],
    data_files=[('libc',['libobnext-mqtt.dylib']), ('libc',['extra.txt'])]
)

#package_dir = {'': 'src'}
#libraries = [('.',{'':'libobnext-mqtt.dylib'})],