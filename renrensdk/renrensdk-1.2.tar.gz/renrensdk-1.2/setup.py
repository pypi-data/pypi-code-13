from distutils.core import setup

NAME = "renrensdk"
DESCRIPTION = "Renren Python3 SDK for social network research."
AUTHOR = "Luping Yu"
AUTHOR_EMAIL = "lazydingding@gmail.com"
URL = "https://github.com/lazydingding/renrensdk"
VERSION = "1.2"

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    # long_description=read("README.md"),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="Apache License, Version 2.0",
    url=URL,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
)
