from setuptools import setup
from setuptools import find_packages

setup(name='componere',
      version='0.1',
      url='https://github.com/premisedata/componere',
      author='Moustafa Maher and Mostafa Gabriel',
      author_email='mmaher@premise.com, mgabriel@premise.com',
      packages=find_packages(),
      install_requires=['graphviz', 'pyyaml'])
