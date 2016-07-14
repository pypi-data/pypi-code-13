from setuptools import setup

files=["resources/*"]

setup(
    # Application name:
    name="BeijingTomorrow",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="Tavis Barr",
    author_email="tavisbarr@gmail.com",

    # Packages
    packages=["beijingtomorrow"],

    package_dir = {'': 'src'},
    
    package_data={'beijingtomorrow': ['resources/*']},
    # Details
    url="http://www.github.com/tavisbarr/BeijingTomorrow",

    #
    # license="LICENSE.txt",
    description="This package generates a beijingtomorrow of the next day's pollution level in Beijing using daily MODIS satellite data and CaffeOnSpark.",

    # long_description=open("README.txt").read(),

)