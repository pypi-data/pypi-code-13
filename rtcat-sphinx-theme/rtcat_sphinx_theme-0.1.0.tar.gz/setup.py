# -*- coding: utf-8 -*-
"""`rtcat_sphinx_theme` lives on `Github`_.

.. _github: https://github.com/RTCat/rtcat_sphinx_theme.git

"""
from setuptools import setup
from rtcat_sphinx_theme import __version__


setup(
    name='rtcat_sphinx_theme',
    version=__version__,
    url='https://github.com/RTCat/rtcat_sphinx_theme.git',
    license='MIT',
    author='Dave Snider, RealTimeCat',
    author_email='dave.snider@gmail.com, info@learning-tech.com',
    description=' Sphinx theme for http://docs.shishimao.com/',
    long_description=open('README.rst').read(),
    zip_safe=False,
    packages=['rtcat_sphinx_theme'],
    package_data={'rtcat_sphinx_theme': [
        'theme.conf',
        '*.html',
        'static/css/*.css',
        'static/js/*.js',
        'static/font/*.*'
    ]},
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Documentation',
        'Topic :: Software Development :: Documentation',
    ],
)
