#!/usr/bin/env python

from distutils.core import setup
from jsoninspectlib import __version__

# PyPi uses reStructuredText but I personally like Markdown. No need for me to write
# things over or succumb to PyPi pressure, we'll just attempt to convert the description
# from MD to rST.
try:
  import pypandoc
  long_description = pypandoc.convert('readme.md', 'rst')
  long_description = long_description.replace("\r", "")
except (IOError, ImportError):
  print("Pandoc not found. Long_description conversion failure.")
  import io
  with io.open('readme.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'json-inspect',
    version = __version__,

    author = 'John Murray',
    author_email = 'me@johnmurray.io',
    description = 'JSON inspection command line client',
    long_description = long_description,
    license='Apache 2.0',
    packages = ['jsoninspectlib'],
    scripts = ['json-inspect'],
    url = 'http://github.com/JohnMurray/json-inspect',
 )
