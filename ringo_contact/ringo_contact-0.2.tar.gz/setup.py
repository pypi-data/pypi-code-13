#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import sys, os


setup(name='ringo_contact',
      version= '0.2',
      description="Contact extension for the ringo webframework",
      long_description="""""",
      classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
      ],
      keywords='ringo pyramid extension',
      author='Torsten Irländer',
      author_email='torsten@irlaender.de',
      url='https://github.com/ringo-framework/ringo_contact',
      license='GNU General Public License v2 or later (GPLv2+)',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'ringo'
      ],
      entry_points="""
      # -*- Entry points: -*-
      [babel.extractors]
          tableconfig = ringo.lib.i18n:extract_i18n_tableconfig
          formconfig = formbar.i18n:extract_i18n_formconfig
          """,
          message_extractors = {'ringo_contact': [
                ('**.py', 'python', None),
                ('**.html', 'mako', None),
                ('**.mako', 'mako', None),
                ('**.xml', 'formconfig', None),
                ('**.json', 'tableconfig', None),
                ('static/**', 'ignore', None)]},

      )
