from distutils.core import setup
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
  long_description = f.read()

setup(
  name = 'easy-aes',
  packages = ['easy-aes'], # this must be the same as the name above
  version = '0.11',
  description = 'An ultra-lightweight library to securely encrypt any file with AES.',
  author = 'Joshua A. Lee',
  author_email = 'jlee17@gmu.edu',
  url = 'https://github.com/Starstorm3/easy-aes', # use the URL to the github repo
  download_url = 'https://github.com/Starstorm3/easy-aes/tarball/0.1', # I'll explain this in a second
  long_description=long_description,
  keywords = ['encryption', 'aes', 'encrypt','advanced encryption standard'], # arbitrary keywords
  license='MIT',
  classifiers=['Development Status :: 3 - Alpha','License :: OSI Approved :: MIT License','Programming Language :: Python :: 3.4',]
)