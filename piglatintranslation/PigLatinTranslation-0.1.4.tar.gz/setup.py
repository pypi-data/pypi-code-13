from setuptools import setup

setup(
    name='PigLatinTranslation',
    version='0.1.4',
    include_package_data=True,
    zip_safe=False,
    url='https://github.com/Jai-Chaudhary/pig-latin-translation-microservice',
    license='MIT',
    author='Jai Chaudhary',
    author_email='jai.chaudhary.ittd@gmail.com',
    packages=['piglatintranslation',],
    install_requires=['Flask'],
    long_description=__doc__,
    description='A Pig Latin Translation Microservice',
    classifiers=[
      "Development Status :: 3 - Alpha",
    ]
)