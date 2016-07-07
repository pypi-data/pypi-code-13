#!/usr/bin/env python2
# coding = utf-8


from setuptools import setup

setup(
    name="qurancorpus",
    description="Arabic Quranic Corpus python API",
    version="0.2.1",
    platforms="ALL",
    license="GPL",
    packages=["qurancorpus"],
    install_requires=['pyparsing'],

    author="Assem Chelli",
    author_email="assem.ch@gmail.com",
    package_dir={'qurancorpus': '.'},
    long_description="""A python api for the Quranic Arabic Corpus project""",
    keywords="quran arabic corpus quranic",

    include_package_data=True,

    package_data = {'qurancorpus': ['quranic-corpus-morpology.xml']},

    zip_safe=False,

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: Arabic",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
