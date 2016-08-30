import runpy
import os
from setuptools import setup, find_packages

ver = runpy.run_path(os.path.join(os.path.dirname(__file__), 'gaunn',
                                  'version.py'))["__version__"]

with open("README.rst") as f:
    long_description = f.read()

setup(
    name='gaunn',
    packages=find_packages(),
    package_data={'': ['*.cu']},
    version=ver,
    description='Feedforward and recurrent networks',
    long_description=long_description,
    author='Gautam.R',
    author_email='gautamrbharadwaj@gmail.com',   
    keywords=['neural network'],
    license="BSD",
   
)
