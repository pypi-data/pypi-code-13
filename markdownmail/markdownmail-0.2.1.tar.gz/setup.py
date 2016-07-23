# -*- coding: utf-8 -*-

from setuptools import setup

_NAME = "markdownmail"

setup(
        name=_NAME,
        description="E-mail with text and html content provided with markdown",
        long_description=open("README").read(),
        version='0.2.1',
        author="Équipe Yaal",
        author_email="contact@yaal.fr",
        url="http://hg." + _NAME + ".yaal.fr",
        packages=[
            _NAME,
        ],
        install_requires=[
            "Markdown==2.6.6",
            "Envelopes==0.4",
        ],
        classifiers=[
            "Programming Language :: Python",
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
        ],      


)

