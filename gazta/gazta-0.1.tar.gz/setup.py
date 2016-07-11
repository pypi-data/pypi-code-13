from setuptools import setup, find_packages
import sys, os
from distutils.command.install import install as _install
import webbrowser

version = '0.1'

class install(_install):
    
    def run(self):
        _install.run(self)
        webbrowser.open('https://www.codesyntax.com/cheese')
        
setup(name='gazta',
      version=version,
      description="'''Win an olympic cheese'''",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='cheese europython2016 codesyntax',
      author='CodeSyntax',
      author_email='info@codesyntax.com',
      url='https://www.codesyntax.com',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      cmdclass={'install': install},
      )
