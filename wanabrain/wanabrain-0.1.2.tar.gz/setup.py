# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(name='wanabrain',
      version='0.1.2',
      description='Deep Learning algorithms for video processing tasks',
      # url='http://github.com/storborg/funniest',
      author='Léo Vetter',
      author_email='vetter.leo@gmail.com',
      license='MIT',
      packages=find_packages(),
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      install_requires=[
            'boto==2.42.0',
      ],
      )