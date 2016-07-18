import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    readme = f.read()

with open(os.path.join(here, 'VERSION')) as f:
    version = f.read().strip()

setup(name='casepro.pods.dummy',
      version=version,
      description=(
          'Example casepro data pod returning statically configured'
          'data'),
      long_description=readme,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Django",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='Praekelt Foundation',
      author_email='dev@praekelt.com',
      url='http://github.com/praekelt/casepro.pods.dummy',
      license='BSD',
      keywords='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      namespace_packages=['casepro', 'casepro.pods'],
      entry_points={})
