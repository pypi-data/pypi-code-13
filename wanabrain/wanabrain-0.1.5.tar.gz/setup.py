# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(name='wanabrain',
      version='0.1.5',
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
            'gensim==0.13.1', 'goslate==1.5.1', 'lmdb==0.89', 'matplotlib==1.5.1', 'MySQL-python==1.2.5', \
            'networkx==1.11', 'nltk==3.2.1', 'numpy==1.11.1', 'protobuf==3.0.0', 'pysmb==1.1.18', 'scikit-image==0.12.3', \
            'requests==2.11.0', 'scikit-learn==0.17.1', 'scipy==0.18.0', 'sk-video==1.1.5', 'sklearn==0.0'
      ],
      )