#from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name='therpy',
    version='0.1dev7',
    #packages=['therpy',],
    packages = find_packages(),
    package_data = {'therpy.Data':['*']},
    license='Open Source',
    author='Parth Patel',
    author_email='pbpatel@mit.edu',
    install_requires=['pyfits','tabulate','tqdm'],
)

# Run following commands on terminal
# python setup.py sdist
# python setup.py register (ONLY FIRST TIME)
# python setup.py sdist upload