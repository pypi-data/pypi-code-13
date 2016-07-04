from setuptools import setup, find_packages

import re

def readme():
    with open('README.rst') as f:
	return f.read()

setup(name='rowingphysics',

      version=re.search(

	  '^__version__\s*=\s*"(.*)"',
	  open('rowingphysics/rowingphysics.py').read(),
	  re.M

	  ).group(1),

      description='Rowing Physics calculations',
      
      long_description=readme(),

      url='http://sanderroosendaal.wordpress.com',

      author='Sander Roosendaal',

      author_email='roosendaalsander@gmail.com',

      license='MIT',

#      py_modules = ['rowingphysics.crew',
#		    'rowingphysics.rowingphysics',
#		    'rowingphysics.rigging'],

      packages=find_packages(),

#      packages = ['rowingphysics','crew','rigging'],
      
      keywords = 'rowing ergometer concept2',
      
      install_requires=[
	  'numpy',
	  'matplotlib',
	  'pandas',
	  ],

      zip_safe=False,
#      include_package_data=True,


      )
