import os

import setuptools

module_path = os.path.join(os.path.dirname(__file__), 'foodutils.py')
version_line = [line for line in open(module_path)
                if line.startswith('__version__')][0]

__version__ = version_line.split('__version__ = ')[-1][1:][:-2]

setuptools.setup(
    name="foodutils",
    version=__version__,
    url="https://github.com/NewmanJ1987/foodutils.git",

    author="Mister foo",
    author_email="mister@foo.com",

    description="Utils for handling food.",
    long_description=open('README.rst').read(),

    py_modules=['foodutils'],
    zip_safe=False,
    platforms='any',

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
