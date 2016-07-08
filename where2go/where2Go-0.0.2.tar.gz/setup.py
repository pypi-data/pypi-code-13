from setuptools import setup, find_packages

with open('README.md') as description:
    long_description = description.read()
    
with open('requirements.txt') as requirements:
    reqs = requirements.read()
    
reqs_list = reqs.split('\n')

setup(
    name="where2Go",
    version="0.0.2",
    author="Georgi Ivanov",
    author_email="georgi.g.ivanov.95@gmail.com",
    description="Your weekend-adventure assistant",
    license="GNU GPL v2",
    keywords=["weekend", "walk", "adventure", "mountain", "nature"],
    packages=["where2Go"],
    long_description=long_description,
    install_requires=reqs_list,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.5",
        "Topic :: Games/Entertainment"
    ]
)
