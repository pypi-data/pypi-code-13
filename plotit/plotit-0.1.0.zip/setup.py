from distutils.core import setup
from platform import platform

setup(
      name             = 'plotit',
      version          = '0.1.0',
      author           = 'meltus',
      author_email     = 'sergiosd@arrakis.es',
      packages         = ['plotit'],
      scripts          = ['bin//print_basic_plot.py'],
      url              = '',
      license          = 'LICENSE.txt',
      platforms        = ['any'],
      description      = 'print a basic plot',
      long_description = open('README.txt').read()
      )



'''
in src directory execute:
> py -3 setup.py sdist
'''
