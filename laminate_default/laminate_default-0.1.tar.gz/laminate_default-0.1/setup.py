"""Laminate Default Theme"""
from setuptools import setup

setup(name='laminate_default',
      version='0.1',
      url='https://github.com/ohenrik/laminate_default',
      description='Default theme for laminate',
      long_description=__doc__,
      author='Ole Henrik Skogstrøm',
      author_email='laminate@amplify.no',
      packages=['laminate_default', 'laminate_default.templates'],
      include_package_data=True,
      install_requires=[],
      classifiers=[
          'Development Status :: 2 - Pre-Alpha'
      ]
     )

__author__ = 'Ole Henrik Skogstrøm'
