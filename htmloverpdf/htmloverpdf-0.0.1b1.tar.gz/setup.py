""""""
from setuptools import setup
from os import path

with open(path.join(path.abspath(path.dirname(__file__)), 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="htmloverpdf",
    version="0.0.1b1",
    description="Render a HTML overlay over existing PDF files",
    long_description=long_description,
    author="Wirehive Ltd",
    author_email="barnaby@wirehive.net",
    url="https://github.com/wirehive/htmloverpdf",
    license='BSD',
    keywords="weasyprint cairo pdf html",
    packages=[
        "htmloverpdf"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3"
    ],
    install_requires=[
        "weasyprint>=0.31",
        "pygobject", #install system packaged not via pip
        "cairocffi", #install system packaged not via pip
        #"cairo" #pip can't even see this one
    ]
)
