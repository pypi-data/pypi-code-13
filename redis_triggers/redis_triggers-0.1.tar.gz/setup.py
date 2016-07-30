from distutils.core import setup

setup(
  name = 'redis_triggers',
  packages = ['redis_triggers'], # this must be the same as the name above
  version = '0.1',
  description = 'Redis Key events that executes a function written by you such as on expiry',
  author = 'Abhishek K gowda',
  author_email = 'abhishek.k6006@gmail.com',
  url = 'https://github.com/abhishek246/redis_triggers.git', # use the URL to the github repo
  download_url = 'https://github.com/abhishek246/redis_triggers.git/tarball/0.1', # I'll explain this in a second
  keywords = ['redis', 'redis-triggers', 'redis_triggers', 'execute function on expiry of a key redis'], # arbitrary keywords
  classifiers = [],
)
