# coding: utf-8

from distutils.core import setup

setup(
        name='twitprof',
        version='0.2.6',
        packages=['twitprof'],
        url='https://github.com/santiavenda2/twitter-scrapper',
        license="Apache License",
        author='Santiago Avendaño',
        author_email='santiavenda2@gmail.com',
        description='Twitter Profile Scrapper',
        install_requires=['tweepy', 'celery[redis]', 'mongoengine', 'flask']
)
