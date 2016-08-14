from distutils.core import setup
setup(
  name = 'pydmm',
  packages = ['core'], 
  version = '0.4',
  description = 'Read data from a dmm',
  long_description=open('README.txt').read(),
  author = 'Michael Weigend',
  author_email = 'mw@creative-informatics.de',
  license='LICENSE.txt',
  url= 'http://pypi.python.org/pypi/pydmm',
#  url = 'https://github.com/mweigend/pydmm', # URL zum GitHub 
#  download_url = 'https://github.com/mweigend/pydmm/tarball/0.1', 
  keywords = ['dmm', 'digital multimeter'], 
)

