#! /usr/bin/env python

import sys

from setuptools import setup , find_packages


setup(name="onyxproject",
      description="Intelligent Dashboard for Raspberry pi",
      long_description=open("README.rst").read(),
      version='0.1',
      packages=find_packages(),
      include_package_data=True,
      url="https://github.com/OnyxProject/Onyx",
      maintainer=("Aituglo"),
      maintainer_email="project@onyxlabs.fr",
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: Web Environment",
          "Intended Audience :: Developers",
          "Intended Audience :: System Administrators",
          "Operating System :: Microsoft :: Windows",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: Build Tools",
          "Topic :: System :: Software Distribution"],
      zip_safe=True,
      entry_points={
          'console_scripts': ['onyx_start=onyx:run','onyx_install=onyx:install','onyx_maj=onyx:maj']
      },
      install_requires=['Flask==0.10.1','Flask-WTF==0.8.3','Flask-sqlalchemy','requests','beautifulsoup4','Flask-Menu','Flask-Login','SQLAlchemy-migrate','flask_bcrypt','flask-Mail','blinker','wikipedia','markupsafe'],
      options={
          'bdist_wheel': {'universal': True},
      },
      platforms=['any'],
      )
