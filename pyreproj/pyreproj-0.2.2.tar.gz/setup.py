import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'DESCRIPTION.rst')) as f:
    DESCRIPTION = f.read()
with open(os.path.join(here, 'CHANGES.rst')) as f:
    CHANGES = f.read()

requires = [
    'pyproj',
    'shapely'
    ]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',  # includes virtualenv
    'pytest-cov',
    ]

setup(name='pyreproj',
      version='0.2.2',
      description='Python Reprojector',
      long_description='\n'.join([
          DESCRIPTION,
          '',
          'Changelog',
          '---------',
          '',
          CHANGES
      ]),
      classifiers=[
          "Programming Language :: Python",
          "Topic :: Scientific/Engineering :: GIS",
          "Topic :: Utilities",
          "Natural Language :: English",
          "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
          "Intended Audience :: Developers",
          "Development Status :: 4 - Beta",
      ],
      author='Karsten Deininger',
      author_email='karsten.deininger@bl.ch',
      url='https://gitlab.com/gf-bl/pyreproj',
      keywords='web proj coordinate transformation',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'testing': tests_require,
      },
      install_requires=requires,
      requires=requires
      )

