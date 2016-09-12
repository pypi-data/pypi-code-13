from setuptools import setup
from pip.req import parse_requirements
from os import path
from codecs import open


here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='buku',
    version='0.0.3',
    description='Powerful command-line bookmark manager. Your mini web!',
    long_description=long_description,
    url='https://github.com/jarun/Buku',
    author='Ovv',
    author_email='ovv@outlook.com',
    license='GPLv3',
    packages=['buku', 'tests', 'auto-completion'],
    zip_safe=False,
    include_package_data=True,
    package_data={'tests': ['ci-test-wrapper'],
                  'auto-completion': ['bash/*', 'fish/*', 'zsh/*']},
    install_requires=['beautifulsoup4>=4.4.1', 'cryptography>=1.3.2'],
)