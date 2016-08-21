"""
setup.py
"""
from setuptools import setup, find_packages

setup(
    name='dici',
    version='0.4.0',
    author='Rodney Gomes',
    author_email='rodneygomes@gmail.com',
    url='',
    install_requires=[],
    tests_require=[
        'robber==1.0.1'
    ],
    test_suite='test',
    keywords=[''],
    py_modules=['dici'],
    packages=find_packages(exclude=['test']),
    license='Apache 2.0 License',
    description='easy to use dict replacement',
    long_description='',
)
