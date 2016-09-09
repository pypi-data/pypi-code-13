#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='kryptal',
      version='0.1.10',
      description='',
      author='Sebastian Messmer',
      author_email='messmer@cryfs.org',
      license='GPLv3',
      url='https://github.com/cryfs/kryptal',
      packages=find_packages(),
      package_data={
          'kryptal.gui': [
              '*.ui'
          ],
          'kryptal.plugins.filesystems': [
              '*.kryptal-plugin'
          ],
          'kryptal.plugins.storageproviders': [
              '*.kryptal-plugin'
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
          'appdirs >= 1.4.0'
      ],
      #keywords = ...,
      classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Environment :: X11 Applications",
        "Environment :: X11 Applications :: Qt",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Communications :: File Sharing",
        "Topic :: Security",
        "Topic :: Security :: Cryptography",
        "Topic :: System :: Filesystems",
        "Topic :: Utilities"
      ]
)
