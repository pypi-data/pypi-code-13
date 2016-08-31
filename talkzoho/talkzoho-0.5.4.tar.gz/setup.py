from setuptools import setup
from setuptools import find_packages


setup(
    name='talkzoho',
    version='0.5.4',
    url='https://github.com/A2Z-Cloud/Talk-Zoho',
    packages=find_packages(exclude=('tests', 'tests.*')),
    setup_requires=['setuptools-markdown'],
    install_requires=[
        'fuzzywuzzy'
        'python-Levenshtein'
        'requests'
        'tornado'],
    long_description_markdown_filename='README.md')
