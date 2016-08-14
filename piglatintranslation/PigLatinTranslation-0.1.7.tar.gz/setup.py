import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='PigLatinTranslation',
    version='0.1.7',
    include_package_data=True,
    zip_safe=False,
    url='https://github.com/Jai-Chaudhary/pig-latin-translation-microservice',
    license='MIT',
    author='Jai Chaudhary',
    author_email='jai.chaudhary.ittd@gmail.com',
    packages=['piglatintranslation',],
    install_requires=['Flask'],
    long_description=read('README.md'),
    description='A Pig Latin Translation Microservice',
    classifiers=[
      "Development Status :: 3 - Alpha",
    ]
)