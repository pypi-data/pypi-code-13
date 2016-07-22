import os
from setuptools import setup, find_packages

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except:
    long_description = ''

classifiers = ['Development Status :: 4 - Beta',
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: Apache Software License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 2.7',
               'Topic :: Software Development',
               'Topic :: System :: Hardware']

setup(
    name         = 'FaBoRTC_PCF2129',
    version      = '1.0.0',
    author       = 'FaBo',
    author_email = 'info@fabo.io',
    description  = "This is a library for the FaBo RTC I2C Brick.",
    long_description=long_description,
    url          = 'https://github.com/FaBoPlatform/FaBoRTC-PCF2129-Python',
    license      = 'Apache License 2.0',
    classifiers  = classifiers,
    packages     = find_packages()
)
