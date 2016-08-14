import os
from setuptools import setup

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

setup(
    name='PigLatinTranslation',
    version='0.1.11',
    include_package_data=True,
    zip_safe=False,
    url='https://github.com/Jai-Chaudhary/pig-latin-translation-microservice',
    license='MIT',
    author='Jai Chaudhary',
    author_email='jai.chaudhary.ittd@gmail.com',
    packages=['piglatintranslation',],
    install_requires=['Flask'],
    long_description=read_md('README.md'),
    description='A Pig Latin Translation Microservice',
    classifiers=[
      "Development Status :: 3 - Alpha",
    ]
)