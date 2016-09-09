#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='kryptal',
      version='0.1.4',
      description='',
      author='Sebastian Messmer',
      author_email='messmer@cryfs.org',
      license='GPLv3',
      url='https://github.com/cryfs/kryptal',
      packages=find_packages(),
      package_data={
          'kryptal.gui': [
              '*.ui'
          ]
      },
      entry_points = {
        'gui_scripts': [
          'kryptal = kryptal.gui.__main__:main'
        ]
      },
      install_requires=[
          'PyQT5 >= 5.7',
          'yapsy >= 1.11.223',
          'jpath >= 1.5'
      ]#,
      #keywords = ...,
      #classifiers=[
      #  "Development Status :: 5 - Production/Stable",
      #  "Environment :: Console",
      #  "Intended Audience :: Developers",
      #  "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
      #  "Programming Language :: Python",
      #  "Programming Language :: C++",
      #  "Topic :: Software Development :: Build Tools",
      #  "Topic :: Software Development :: Code Generators",
      #  "Topic :: Software Development :: Version Control"
      #]
)
