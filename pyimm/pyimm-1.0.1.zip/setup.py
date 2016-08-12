'''
 Copyright (c) 2014, UChicago Argonne, LLC
 See LICENSE file.
'''
from setuptools import setup

setup(name='pyimm',
      version='1.0.1',
      description='Python Program to read IMM data files from XPCS beamlines ' +
                'at the Advanced Photon Source',
      author = 'John Hammonds, Benjamin Pausma, Timothy Madden',
      author_email = 'JPHammonds@anl.gov',
      url = 'https://confluence.aps.anl.gov/',
      packages = ['pyimm',
                  'dev', 
                  'test',
                  'testData'] ,
      license = 'See LICENSE File',
      platforms = 'any',
      )