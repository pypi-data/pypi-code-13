from distutils.core import setup
from setuptools import find_packages
from distutils.core import Extension
#from setuptools import setup, find_packages
setup(
    name = 'altugstestpackage',
    packages = find_packages(),
    package_data={'': ['extra.txt']},
    version = '0.1.1',
    description = 'A Python package example',
    author = 'altugb',
    author_email = 'altug.bitlislioglu@epfl.ch',
    url = 'https://altugb@bitbucket.org/altugb/testpackage.git',    
    py_modules=['altugstestpackage'],
    data_files=[('libc',['libobnext-mqtt.dylib']), ('libc',['extra.txt'])]
)

#package_dir = {'': 'src'}
#libraries = [('.',{'':'libobnext-mqtt.dylib'})],