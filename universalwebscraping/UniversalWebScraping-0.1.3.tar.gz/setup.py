from setuptools import setup, find_packages
import sys, os

version = '0.1.3'

setup(name='UniversalWebScraping',
      version = version,
      description="universal web scraping",
      long_description="""\
universal web scraping""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='scraping',
      author='Zulu Ng',
      author_email='ngz1357@gmail.com',
      url='http://lazcode.com',
      license='mit',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
