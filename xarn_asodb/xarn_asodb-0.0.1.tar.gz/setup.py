from setuptools import setup

setup(
    name='xarn_asodb',
    version='0.0.1',
    url='https://bitbucket.org/dagnelies/asodb',
    author='Arnaud Dagnelies',
    author_email='arnaud.dagnelies@gmail.com',
    license='Proprietary',
    keywords='',
    packages=['asodb'],
    install_requires=[
        'bottle',
        'canister',
        'pysos',
        'starpath'
    ],
)