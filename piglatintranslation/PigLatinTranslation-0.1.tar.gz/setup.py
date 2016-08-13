from distutils.core import setup

setup(
    name='PigLatinTranslation',
    version='0.1',
    include_package_data=True,
    url='https://github.com/Jai-Chaudhary/pig-latin-translation-microservice',
    license='MIT',
    author='Jai Chaudhary',
    author_email='jai.chaudhary.ittd@gmail.com',
    packages=['app',],
    long_description=__doc__,
    description='A Pig Latin Translation Microservice',
)