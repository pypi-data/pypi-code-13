from distutils.core import setup
setup(
  name = 'shipwire',
  packages = ['shipwire'], # this must be the same as the name above
  version = '0.9.1',
  description = 'A Python abstraction layer around the Shipwire API.',
  author = 'Neil Durbin, Clark Fischer',
  author_email = 'neildurbin@gmail.com',
  url = 'https://github.com/durbin/shipwire-python',
  download_url = 'https://github.com/durbin/shipwire-python/archive/master.tar.gz',
  keywords = ['shipwire', 'api', 'wrapper'],
  classifiers = [],
  install_requires = ['requests >= 2.4.3'],
)
