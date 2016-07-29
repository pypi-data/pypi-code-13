#!/usr/bin/env python
try:    
    from setuptools import setup, find_packages
except:    
    from distutils.core import setup, find_packages
 
setup(name='flask_base64_msm_session',
      version='1.0',
      description='Use base64 encoder on memcached server. And it will use memcached on session',
      author='Sparrow Jang',
      author_email='sparrow.jang@gmail.com',
      url='https://github.com/eHanlin/flask_base64_msm_session',
      packages=find_packages(),
      install_requires=['pylibmc', 'msm-transcoder', 'msm_api']
     )   

