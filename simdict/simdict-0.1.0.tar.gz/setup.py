import codecs
from setuptools import setup, find_packages
import simdict


def long_description():
    with codecs.open('README.md', 'r') as f:
        return f.read()

version = simdict.__version__
setup(
    name="simdict",
    version=version,
    packages=find_packages(),
    long_description=long_description(),
    install_requires=['requests>=2.7.0'],
    author="4cat",
    author_email="4catcode@gmail.com",
    description="This is a simple English - Chinese dictionary",
    license="MIT",
    keywords="dictionary",
    url="https://github.com/4cat/simdict",
    entry_points={
        'console_scripts': ['simdict = simdict.core:main'],
    },
)
