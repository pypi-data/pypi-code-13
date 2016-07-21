from setuptools import setup

setup(
    name = 'pyagram',
    version = '1.0.2',
    description = 'Pyagram: Python Finite State Machine Diagram Generator',
    author = 'Hideshi Ogoshi',
    author_email = 'hideshi.ogoshi@gmail.com',
    url = 'https://github.com/hideshi',
    packages = ['pyagram'],
    install_requires=[
        'pyparsing',
    ],
    entry_points = {
        'console_scripts': ['pyagram = pyagram.pyagram:main']
    },
)
