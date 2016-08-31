from setuptools import setup
from setuptools import find_packages


setup(
    name='talkzoho',
    version='0.5.9',
    description='Asynchronous Wrapper for Zoho\'s Numerous APIs',
    url='https://github.com/A2Z-Cloud/Talk-Zoho',
    packages=find_packages(exclude=('tests', 'tests.*')),
    install_requires=[
        'fuzzywuzzy',
        'python-Levenshtein',
        'requests',
        'tornado'])
