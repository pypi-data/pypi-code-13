""" Install
"""
from setuptools import setup, find_packages

PACKAGE_NAME = "xlserver"
PACKAGE_VERSION = "1.1"
SUMMARY = (
    "Simple Server HTTP for reading *.xls and *.xlsx files. "
)
DESCRIPTION = (
    open("README.rst", 'r').read()
)

setup(name=PACKAGE_NAME,
      version=PACKAGE_VERSION,
      description=SUMMARY,
      long_description=DESCRIPTION,
      author='Catalin Mititiuc',
      author_email='mititiuc.cata@gmail.com',
      url='https://github.com/catalinmititiuc/xlserver',
      license='GPLv2',
      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      entry_points = {
          'console_scripts': [
              'xlserver = xlserver.xlserver:main',
          ]},
      classifiers=[
          'Environment :: Console',
          'Intended Audience :: Developers',
          "Programming Language :: Python",
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Libraries :: Python Modules',
          ],
      install_requires=[
          'xlrd',
          ],
)
