from setuptools import setup

setup(
  name = 'lablackey',
  packages = ['lablackey','lablackey.db'], # this must be the same as the name above
  version = '0.1.2a',
  description = 'A collection of tools for django',
  author = 'Chris Cauley',
  author_email = 'chris@lablackey.com',
  url = 'https://github.com/chriscauley/lablackey', # use the URL to the github repo
  keywords = ['utils'], # arbitrary keywords
  license = 'GPL',
  include_package_data = True,
)
