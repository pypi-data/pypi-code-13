from setuptools import setup

setup(
    # Application name:
    name='pyrml',

    # Version number (initial):
    version='0.1.4',

    # Application author details:
    author='Rodolfo Castillo',
    author_email='rcvallada@gmail.com',

    # Details
    url='http://rainbot.info/rmls#Python',

    description='RainBot Module Library for Python',

    # Requires
    install_requires=[
        'json-rpc'
    ],

    # Dependent packages (distributions)
    packages=[
        'pyrml',
    ],
)
