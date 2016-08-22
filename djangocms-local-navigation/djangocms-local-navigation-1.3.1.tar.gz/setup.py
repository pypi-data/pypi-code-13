#!/usr/bin/env python
from setuptools import setup
from djangocms_local_navigation import __version__


install_requires = [
    'django-cms>=3.0',
    'beautifulsoup4',
    'djangocms-text-ckeditor',
]


setup(
    name='djangocms-local-navigation',
    version=__version__,
    packages=['djangocms_local_navigation'],
    description="Provides a local navigation plugin in your pages",
    author='Sylvain Fankhauser',
    author_email='sylvain.fankhauser@liip.ch',
    url='https://github.com/sephii/djangocms-local-navigation',
    install_requires=install_requires,
    license='BSD',
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
