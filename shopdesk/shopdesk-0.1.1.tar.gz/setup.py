#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import setuptools

setuptools.setup(
    name = "shopdesk",
    version = "0.1.1",
    author = "Hive Solutions Lda.",
    author_email = "development@hive.pt",
    description = "Shopdesk Retail System",
    license = "Apache License, Version 2.0",
    keywords = "shopdesk retail payments",
    url = "http://shopdesk.hive.pt",
    zip_safe = False,
    packages = [
        "shopdesk",
        "shopdesk.controllers",
        "shopdesk.models",
        "shopdesk.test"
    ],
    test_suite = "shopdesk.test",
    package_dir = {
        "" : os.path.normpath("src")
    },
    package_data = {
        "budy" : [
            "static/css/*.css",
            "static/images/*",
            "static/images/email/*",
            "static/js/*.js",
            "templates/*.tpl",
            "templates/email/*.tpl"
        ]
    },
    install_requires = [
        "appier",
        "appier_extras"
    ],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5"
    ]
)
