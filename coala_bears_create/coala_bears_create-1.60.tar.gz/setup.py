#!/usr/bin/env python
# Work around mbcs bug in distutils.
# http://bugs.python.org/issue10945
import codecs
try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    func = lambda name, enc=ascii: {True: enc}.get(name=='mbcs')
    codecs.register(func)
from setuptools import setup, find_packages


def readme():
    with open('README.rst') as f:
        return f.read()


def requirements():
    with open('requirements.txt') as f:
        return f.read().splitlines()


version = '1.60'


setup(
    name='coala_bears_create',
    version=version,
    install_requires=requirements(),
    author="The coala developers",
    maintainer="Karan Sharma",
    author_email='karansharma1295@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    url='https://gitlab.com/coala/coala-bear-management',
    license='GNU Affero General Public License v3 or later (AGPLv3+)',
    description='CLI tool to create coala bears by answering few simple questions',
    entry_points={
        'console_scripts': [
            'coala-bears-create = coala_bears_create.coala_bears_create:main',
        ],
    },
    long_description=readme(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
