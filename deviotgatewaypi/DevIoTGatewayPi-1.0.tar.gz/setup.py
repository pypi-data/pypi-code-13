from distutils.core import setup
setup(
  name = 'DevIoTGatewayPi',
  packages = ['DevIoTGatewayPi'], # this must be the same as the name above
  version = '1.0',
  description = 'Quickly help user to build DevIot Gateway service for Pi',
  author = 'Tingxin Xu',
  author_email = 'tingxxxu@cisco.com',
  url = 'https://github.com/tingxin/DevIoT_Pi_SDK', # use the URL to the github repo
  download_url = 'https://github.com/tingxin/DevIoT_Pi_SDK/tree/master/DevIoTGatewayPi', # I'll explain this in a second
  keywords = ['Gateway', 'DevIot', 'Cisco'], # arbitrary keywords
  classifiers = [],
  install_requires=[
        "DevIoTGateway"
    ]
)
