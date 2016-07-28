#!/usr/bin/env python
try:    
    from setuptools import setup, find_packages
except:    
    from distutils.core import setup, find_packages
 
setup(name='msm_api',
      version='1.4',
      description='Use base64 encoder on memcached server.',
      author='Sparrow Jang',
      author_email='sparrow.jang@gmail.com',
      url='https://github.com/eHanlin/msm_api',
      packages=find_packages(),
      install_requires=['pylibmc', 'msm-transcoder']
     )   

