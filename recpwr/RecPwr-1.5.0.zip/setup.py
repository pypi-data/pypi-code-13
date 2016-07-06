import setuptools
from distutils.core import setup

setup(
    # Application name:
    name="RecPwr",

    # Version number (initial):
    version="1.5.0",

    # Application author details:
    author="Eric Haberland",
    author_email="ehaberland@lightningpacks.com",

    # Packages
    packages=["RecPwr"],

    # Include additional files into the package
    # include_package_data=True,
    package_data = {'':['*.xlsx', '*.psdata', '*.psmacro', '*.bat', '*/LP Power Data'],

    },

    # Details
    url="https://github.com/haberlae/power_tester",

    download_url='https://github.com/haberlae/power_tester/tarball/1.5.0',

    #
    license="LICENSE.txt",
    description="RecPwr measurements",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "PyAutoIt", 
        "easygui==0.97.4",
        "openpyxl",
        "matplotlib",
        "NumPy", 
        
    ],
)