#!/usr/bin/env python   
try:                    
    from setuptools import setup, find_packages
except:                 
    from distutils.core import setup, find_packages

setup(name='msm_transcoder',
      version='1.2',
      description='Encode and decode base64 data to binary data.',
      author='Sparrow Jang',
      author_email='sparrow.jang@gmail.com',
      url='https://github.com/eHanlin/msm-transcoder-python',
      packages=find_packages(),
     )

