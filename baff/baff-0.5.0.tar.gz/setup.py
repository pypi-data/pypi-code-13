import os
import sys

import baff

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension
    pass

packages = [
    'baff'
]

requires = []
setup(
    name='baff',
    version=baff.__version__,
    description='Process spawner and monitor',
    long_description=open('README.txt').read(),
    author='Gamaliel Espinoza Macedo',
    author_email='gamaliel.espinoza@gmail.com',
    url='https://bitbucket.org/gamikun/baff',
    packages=packages,
    package_dir={'baff': 'baff'},
    install_requires=requires,
    include_package_data=True,
    package_data={},
    ext_modules=[],
    zip_safe=False,
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ),
)