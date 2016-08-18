# coding=utf-8
import os

from setuptools import setup

setup(
    name='django-simple-news-app',
    version='0.1.3',
    zip_safe=False,
    description='Generic news application for Django',
    long_description=open(os.path.join(os.path.dirname(__file__),
                                       'README.rst')).read(),
    author='Evgeny Barbashov',
    author_email='evgenybarbashov@yandex.ru',
    url='https://github.com/bzzzzzz/django-simple-news-app',
    packages=[
        'django_news',
        'django_news.tests',
        'django_news.migrations',
        'django_news.templatetags',
    ],
    package_data={
        'django_news': [
            'locale/*/LC_MESSAGES/*.po',
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities',
    ],
    install_requires=[
        'django>=1.8',
        'django-ckeditor>=5.0'
    ],
)
