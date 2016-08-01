#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='cover-rage-server',
    version='0.0.2',
    description='Utility (server) to check coverage for the last commit / pull request while running tests on CI.',
    long_description=open('README.md', 'r').read(),
    author='Alexander Ryabtsev',
    author_email='ryabtsev.alexander@gmail.com',
    url='https://github.com/alexryabtsev/cover_rage_server',
    packages=['cover_rage_server'],
    entry_points={
        'console_scripts': ['rage_cli=cover_rage_server.rage_cli:__main__'],
    },
    install_requires=open('requirements.txt', 'r').readlines(),
    license='MIT',
    classifiers=(
        b'Development Status :: 3 - Alpha',
        b'Environment :: Console',
        b'Intended Audience :: Developers',
        b'License :: OSI Approved :: MIT License',
        b'Natural Language :: English',
        b'Operating System :: OS Independent',
        b'Programming Language :: Python',
        b'Programming Language :: Python :: 3.5',
        b'Topic :: Software Development :: Testing',
    ),
)
