# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='keyw',
    version='1.0',

    author='Kazaryan Sargis',
    author_email='basandbuddy@mail.ru',

    url='https://github.com/YaSargis/keyw-1.0',
    description='layout and transcription from rus to eng, eng to rus, eng to am, am to rus',

    packages=find_packages(),
    install_requires=['peppercorn'],

    license='MIT License',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Text Processing :: Linguistic :: Python Modules',
    ],
    keywords='Armenian Russian English layout-changer transcription ',
)
