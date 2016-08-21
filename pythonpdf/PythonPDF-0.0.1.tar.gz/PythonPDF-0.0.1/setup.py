from setuptools import setup, find_packages

setup(
    name='PythonPDF',
    version='0.0.1',
    packages=find_packages(exclude=["tests"]),
    url='https://github.com/Heasummn/PyPDF',
    license='MIT',
    author='Heasummn and Suswombat',
    author_email='heasummn@gmail.com',
    description='A small library for creating PDF files using Python'
)
