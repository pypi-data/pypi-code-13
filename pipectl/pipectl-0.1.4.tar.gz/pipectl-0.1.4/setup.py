# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from pip.req import parse_requirements


install_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]



setup(
    name="pipectl",
    version="0.1.4",
    description="A CI/CD Build pipeline DSL",
    license="MIT",
    author="adamar",
    author_email="none@none.com",
    url="http://github.com/adamar/pipectl",
    packages=find_packages(),
    install_requires=reqs,
    scripts=['pipectl/pipectl'],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ]
)
