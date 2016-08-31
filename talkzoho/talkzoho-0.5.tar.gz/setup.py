from distutils.core import setup
from setuptools import find_packages
from pip.req import parse_requirements as parse


setup(
    name='talkzoho',
    version='0.5',
    url='https://github.com/A2Z-Cloud/Talk-Zoho',
    packages=find_packages(exclude=('tests', 'tests.*')),
    long_description=open('README.md').read(),
    install_requires=[str(r.req) for r in parse('requirements/production.txt', session=False)],  # noqa
)
