# python setup.py register -r pypitest
# python setup.py sdist upload -r pypitest
# python setup.py register -r pypi
# python setup.py sdist upload -r pypi

# python ryan/ryan.py 
# python setup.py sdist upload -r pypi
# sudo pip install --upgrade ryan

from distutils.core import setup
setup(
  name = 'ryan',
  packages = ['ryan'],
  version = '0.0.14',
  description = 'Common Python Tools',
  author = 'Ryan Smith',
  author_email = 'rms1000watt@gmail.com',
  url = 'https://github.com/rms1000watt/ryan-project',
  keywords = ['logging', 'tools'], 
  classifiers = [],
)