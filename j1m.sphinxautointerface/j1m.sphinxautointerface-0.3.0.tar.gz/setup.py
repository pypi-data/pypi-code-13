# -*- coding: utf-8 -*-

name = 'j1m.sphinxautointerface'
version = '0.3.0'

from setuptools import setup, find_packages

long_desc = '''
This package contains a fork of the zopeext Sphinx extension.

Original documentation: http://packages.python.org/sphinxcontrib-zopeext

Install with ``pip install j1m.sphinxautointerface``.

To use this extension, include `'j1m.sphinxautointerface'` in your
`extensions` list in the `conf.py` file for your documentation.

This provides some support for Zope interfaces by providing an `autointerface`
directive that acts like `autoclass` except uses the Zope interface methods for
attribute and method lookup (the interface mechanism hides the attributes and
method so the usual `autoclass` directive fails.)  Interfaces are intended
to be very different beasts than regular python classes, and as a result require
customized access to documentation, signatures etc.

See Also
--------
* http://sphinx.pocoo.org/
* http://sphinx.pocoo.org/ext/autodoc.html
* http://docs.zope.org/zope.interface/README.html
* http://packages.python.org/sphinxcontrib-zopeext/

'''

requires = ['Sphinx>=0.6', 'zope.interface', 'setuptools']

from setuptools import setup

setup(
    name=name, version=version,
    url='http://bitbucket.org/j1m/sphinxautointerface',
    license='BSD',
    author='Michael McNeil Forbes and Jim Fultom',
    author_email='jim@jimfulton.info',
    description='Sphinx extension for documenting zope.interface interfaces',
    long_description=long_desc,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Zope3',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['j1m'],
)
