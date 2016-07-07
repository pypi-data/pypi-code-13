import re
from setuptools import setup
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))

with open('rbpy/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)
with open('rbpy/__init__.py', 'r') as fd:
    author = re.search(r'^__author__\s*=\s*[\'"]([^\'"]*)[\'"]',
                       fd.read(), re.MULTILINE).group(1)
with open('rbpy/__init__.py', 'r') as fd:
    license = re.search(r'^__license__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# get the dependencies and installs
with open(path.join(here, 'requirements/core.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')
with open(path.join(here, 'requirements/dev.txt'), encoding='utf-8') as f:
    all_test_reqs = f.read().split('\n')[1:]
install_requires = [x.strip() for x in all_reqs if 'git+' not in x]
install_test_requires = [x.strip() for x in all_test_reqs if 'git+' not in x]

setup(
    name='rbpy',
    version=version,
    description='Python wrapper around the RelayBox API.',
    long_description=long_description,
    url='https://github.com/mmaybeno/rbpy',
    download_url='https://bitbucket.org/relaybox/rbpy/get/master.tar.gz',
    license=license,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    keywords='Relay Box',
    packages=['rbpy'],
    include_package_data=True,
    author=author,
    author_email='mmaybeno@gmail.com',
    install_requires=install_requires,
    test_suite='tests',
    tests_require=install_test_requires
)
