from setuptools import find_packages
from distutils.core import setup

try:
  import pypandoc
  LONG_DESCRIPTION = pypandoc.convert('README.md', 'rst')
  LONG_DESCRIPTION += '\n' + pypandoc.convert('CHANGELOG.md', 'rst')
except(IOError, ImportError, OSError):
  LONG_DESCRIPTION = open('README.md').read()
  LONG_DESCRIPTION += open('CHANGELOG.md').read()

setup(
  author = 'Jorge Alpedrinha Ramos',
  author_email = 'python@uphold.com',
  description = 'AioPype - Flow based programming with asyncio',
  install_requires = [
    'aiohttp==0.21.2',
    'pusherclient==0.3.0',
    'pyee==1.0.2',
    'raven==5.11.0',
    'websocket-client==0.37.0',
    'websockets==3.0',
  ],
  license = 'LICENSE',
  long_description = LONG_DESCRIPTION,
  name = 'aiopype',
  package_data = { '': ['*.yml']},
  packages = find_packages(),
  url = 'https://www.github.com/uphold/aiopype/',
  version = '0.1.3',
)
