#from distutils.core import setup
#from setuptools import find_packages
#from distutils.core import Extension
from setuptools import find_packages
from distutils.core import setup
setup(
    name = 'altugssecondtest',
    packages = find_packages(),
    version = '0.2.0',
    description = 'A Python package example',
    author = 'altugb',
    author_email = 'altug.bitlislioglu@epfl.ch',
    url = 'https://altugb@bitbucket.org/altugb/altugssecondtest.git',    
    py_modules=['altugssecondtest'],    
    package_data={'': ['libobnext-mqtt.dylib','extra.txt']},
    include_package_data=True,
    install_requires=[],
)

#package_dir = {'': 'src'}
#libraries = [('.',{'':'libobnext-mqtt.dylib'})],
#data_files=[('libc',['/libobnext-mqtt.dylib']), ('libc',['/extra.txt'])],