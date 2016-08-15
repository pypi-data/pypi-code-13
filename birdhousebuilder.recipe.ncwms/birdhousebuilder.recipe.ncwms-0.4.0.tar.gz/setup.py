# -*- coding: utf-8 -*-
"""
This module contains the tool of birdhousebuilder.recipe.ncwms
"""
from setuptools import find_packages
from setuptools import setup

name = 'birdhousebuilder.recipe.ncwms'

version = '0.4.0'
description = 'A Buildout recipe to install and configure ncWMS2 server with Anaconda.'
long_description = (
    open('README.rst').read() + '\n' +
    open('AUTHORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

entry_points = '''
[zc.buildout]
default = %(name)s:Recipe
[zc.buildout.uninstall]
default = %(name)s:uninstall
''' % globals()

reqs = ['setuptools',
        'zc.buildout',
        'zc.recipe.deployment >=1.3.0',
        'Mako',
        'birdhousebuilder.recipe.conda >=0.3.1',
        'birdhousebuilder.recipe.tomcat >=0.3.0',]
tests_reqs = ['zc.buildout', 'zope.testing']


setup(name=name,
      version=version,
      description=description,
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Framework :: Buildout',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'License :: OSI Approved :: BSD License',
      ],
      keywords='buildout recipe wms ncwms tomcat birdhouse conda anaconda',
      author='Birdhouse',
      author_email='wps-dev at dkrz.de',
      url='https://github.com/bird-house/birdhousebuilder.recipe.ncwms',
      license='Apache License 2',
      install_requires = reqs,
      extras_require = dict(tests=tests_reqs),
      entry_points=entry_points,
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['birdhousebuilder', 'birdhousebuilder.recipe'],
      include_package_data=True,
      zip_safe=False,
      )
