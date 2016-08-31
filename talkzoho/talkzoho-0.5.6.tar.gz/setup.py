from setuptools import setup
from setuptools import find_packages


setup(
    name='talkzoho',
    version='0.5.6',
    url='https://github.com/A2Z-Cloud/Talk-Zoho',
    packages=find_packages(exclude=('tests', 'tests.*')),
    install_requires=[
        'fuzzywuzzy'
        'python-Levenshtein'
        'requests'
        'tornado'],
    package_data={
        '': 'README.md'},
    long_description=open('README.md').read())
