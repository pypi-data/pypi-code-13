from setuptools import setup

setup(
  name = 'arclist',
  packages = ['arclist'], # this must be the same as the name above
  version = '0.4.1',
  description = 'lists open phabricator diffs and their build / accept statuses',
  author = 'Brendan Ryan',
  author_email = 'ryan.brendanjohn@gmail.com',
  url = 'https://github.com/bjryan2/arclist',
  download_url = 'https://github.com/bjryan2/arclist',
  keywords = [],
  classifiers = [],
  entry_points = {
        'console_scripts': [
            'arclist = arclist.cmd:main'
        ]
    },
)
