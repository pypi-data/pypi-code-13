from distutils.core import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

try:
  with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()
except FileNotFoundError:
  long_description = ""
  print("WARNING: DESCRIPTION FILE NOT FOUND")
setup(
  name = 'aespy',
  packages = ['aespy'],
  version = '0.131',
  description = 'An ultra-lightweight library to securely encrypt any file with AES.',
  author = 'Joshua A. Lee',
  author_email = 'jlee17@gmu.edu',
  url = 'https://github.com/Starstorm3/aespy.git',
  download_url = 'https://github.com/pypa/sampleproject/archive/master.zip',
  long_description=long_description,
  keywords = ['encryption', 'aes', 'encrypt','advanced encryption standard'],
  license='MIT',
  classifiers=['Development Status :: 3 - Alpha','License :: OSI Approved :: MIT License','Programming Language :: Python :: 3.4',]
)