from distutils.core import setup

setup(
  name = 'my_funky_package',
  packages = ['my_funky_package'], # this must be the same as the name above #???
  version = '0.7',
  description = 'A random test lib',
  author = 'Umut Orman',
  author_email = 'umutormans@gmail.com',
  url = 'https://github.com/UmutOrman/mypackage', # use the URL to the github repo
  download_url = 'https://github.com/UmutOrman/mypackage/tarball/0.1', # I'll explain this in a second
  keywords = ['testing', 'logging', 'example'], # arbitrary keywords
  classifiers = [],
)
