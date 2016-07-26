from distutils.core import setup
setup(
  name = 'gitpanion',
  packages = ['gitpanion/github_api'], # this must be the same as the name above
  version = '1.0.0.2',
  description = 'A module to make using the github v3 REST api in python 3 easy.',
  author = 'Calder White',
  author_email = 'calderwhite1@gmail.com',
  url = 'https://github.com/CalderWhite/gitpanion', # use the URL to the github repo
  download_url = 'https://github.com/CalderWhite/gitpanion/archive/master.zip', # I'll explain this in a second
  keywords = [], # arbitrary keywords
  classifiers = [],
)
