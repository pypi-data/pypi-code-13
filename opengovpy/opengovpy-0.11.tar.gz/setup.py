# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='opengovpy',
    version='0.011',
    description='Python wrapper around http://api.data.mos.ru/',
    license='BSD',
    url='https://github.com/AntonKorobkov/opengovpy',
    author='Anton Korobkov',
    author_email='korobq@gmail.com',
    keywords='api opendata',
    packages=find_packages(exclude=['tests']),
    install_requires=['requests']
)
