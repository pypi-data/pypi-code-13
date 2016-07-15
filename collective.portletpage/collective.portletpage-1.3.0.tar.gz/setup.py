# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup
import os

version = '1.3.0'

setup(name='collective.portletpage',
      version=version,
      description="A Plone page that can contain portlets",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.rst")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 5.0",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone portlet content',
      author='Martin Aspeli',
      author_email='optilude@gmail.com',
      maintainer='Luca Fabbri',
      maintainer_email='luca@keul.it',
      url='https://github.com/collective/collective.portletpage',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'Products.CMFPlone',
        'plone.portlets',
        'plone.app.portlets',
        'archetypes.configure',
      ],
      extras_require={
        'test': [
            'plone.app.testing[robot]>=4.2.2',
            'plone.app.robotframework',
            'plone.testing',
        ],
       },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
