from distutils.core import setup

setup(
  name = 'hackerrank',
  packages = ['hackerrank'],
  version = '0.1',
  description = 'An unofficial python SDK for interacting with HackerRank for Work',
  author = 'Jonathan I. Davila',
  author_email = 'jonathan@davila.io',
  url = 'https://github.com/defionscode/hacker_rank_fw',
  download_url = 'https://github.com/peterldowns/mypackage/tarball/0.1',
  keywords = ['hackerrank', 'hacker rank', 'interviewing'],
  license = 'LICENSE', 
  install_requires = [
      'pypandoc==1.2.0',
      'requests==2.11.1'
  ],
  classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'Natural Language :: English',
    'Operating System :: OS Independent',
  ],
)
