# coding: utf-8

from distutils.core import setup

setup(
        name='twitprof',
        version='0.2.1',
        packages=['twitprof'],
        url='https://github.com/santiavenda2/twitter-scrapper',
        license=open('LICENSE').read(),
        author='Santiago Avendaño',
        author_email='santiavenda2@gmail.com',
        description='Twitter Profile Scrapper',
        long_description=open('README.md').read(),
        install_requires=open('requirements.txt').read().splitlines(),
        package_data={'': ['requirements.txt', 'LICENSE', 'README.rst']},
        include_package_data=True,
)
