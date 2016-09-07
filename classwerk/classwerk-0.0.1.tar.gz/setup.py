from setuptools import find_packages
from setuptools import setup

from classwerk import __version__


setup(
    name='classwerk',
    version=__version__,
    provides=["classwerk"],
    author='Keshav Varma',
    author_email='keshavdv@gmail.com',
    description='Github automation tools for classrooms',
    packages=find_packages(exclude=("tests*", "scripts*")),
    include_package_data=True,
    install_requires=[
        'gitpython >= 2.0.8',
        'pyyaml >= 3.0',
        'github3.py >= 0.9.5',
        'travispy >= 0.3.5',
        'selenium >= 2.0.0',
    ],
    entry_points={'console_scripts': [
        'classwerk=classwerk.classwerk:main',
    ]},
)