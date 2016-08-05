from distutils.core import setup
setup(
  name = 'simplepush',
  packages = ['simplepush'],
  version = '0.1',
  description = 'SimplePush python library',
  author = 'SimplePush.io',
  author_email = 'contact@simplepush.io',
  url = 'https://simplepush.io',
  keywords = ['push', 'notification', 'logging', 'app', 'simple'],
  license = 'MIT',
  install_requires=[
        'requests',
      ],
  classifiers = [],
)
