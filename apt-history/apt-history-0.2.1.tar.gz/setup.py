from distutils.core import setup
setup(
  name = 'apt-history',
  packages = ['apt-history'],
  version = '0.2.1',
  description = 'apt history script',
  author = 'Antti Leppa',
  author_email = 'antti.leppa@metatavu.fi',
  url = 'https://github.com/Metatavu/apt-history',
  download_url = 'https://github.com/Metatavu/apt-history/tarball/0.2.1', 
  keywords = ['apt'],
  classifiers = [],
  scripts = ['apt-history/main.py'],
  entry_points={
    'console_scripts': [
      'apt-history=apt-history:main',
    ],
  },
)