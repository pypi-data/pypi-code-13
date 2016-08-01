from setuptools import setup

import os
long_description = 'Shortcuts for saving and exporting matplotlib plots.'
if os.path.exists('README.txt'):
    long_description = open('README.txt').read()

setup(
    name='matplotsave',
    author='Christopher Chen',
    author_email='christopher.chen1995@gmail.com',
    version='0.1.2',
    description="""Helper functions and context manager to make it easier to save matplotlib plots as images.""",
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Operating System :: OS Independent",
    ],
    keywords="matplotlib save export images context managers functions",
    url='https://bitbucket.org/TheCDC/matplotsave',
    license='Public Domain',
    packages=['matplotsave'],
    download_url="https://bitbucket.org/TheCDC/matplotsave/get/HEAD.zip",
    install_requires=[],
    zip_safe=True
)
