from setuptools import setup, find_packages


setup(
    name='xarn_asodb',
    version='0.0.2',
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