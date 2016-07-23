"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of toktokkie.

    toktokkie is a program that allows convenient managing of various
    local media collections, mostly focused on video.

    toktokkie is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    toktokkie is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with toktokkie.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

# imports
import os
import sys
import platform
from setuptools import setup, find_packages
import toktokkie.metadata as metadata

if platform.system() == "Windows":
    # noinspection PyUnresolvedReferences
    import py2exe


def readme():
    """
    Reads the readme file.

    :return: the readme file as a string
    """
    try:
        # noinspection PyPackageRequirements
        import pypandoc
        with open('README.md') as f:
            # Convert markdown file to rst
            markdown = f.read()
            rst = pypandoc.convert(markdown, 'rst', format='md')
            return rst
    except (OSError, ImportError):
        # If pandoc is not installed, just return the raw markdown text
        with open('README.md') as f:
            return f.read()


def find_scripts():
    """
    Returns a list of scripts in the bin directory

    :return: the list of scripts
    """
    scripts = []
    for file_name in os.listdir("bin"):
        if not file_name == "__init__.py" and os.path.isfile(os.path.join("bin", file_name)):
            scripts.append(os.path.join("bin", file_name))
    return scripts

if platform.system() == "Windows" and sys.argv[1] == "py2exe":
    setup(console=["bin/toktokkie"],
          windows=["bin/toktokkie-tk"],
          zipfile=None,
          name=metadata.project_name,
          version=metadata.version_number,
          description=metadata.project_description,
          long_description=readme(),
          classifiers=[metadata.development_status,
                       metadata.audience,
                       metadata.license_identifier,
                       metadata.topic,
                       metadata.language,
                       metadata.compatible_os,
                       metadata.environment
                       ] + metadata.programming_languages,
          url=metadata.project_url,
          download_url=metadata.download_url,
          author=metadata.author_name,
          author_email=metadata.author_email,
          license=metadata.license_type,
          packages=find_packages(),
          install_requires=metadata.dependencies,
          dependency_links=[],
          test_suite='nose.collector',
          tests_require=['nose'],
          scripts=find_scripts(),
          zip_safe=False)

else:
    setup(name=metadata.project_name,
          version=metadata.version_number,
          description=metadata.project_description,
          long_description=readme(),
          classifiers=[metadata.development_status,
                       metadata.audience,
                       metadata.license_identifier,
                       metadata.topic,
                       metadata.language,
                       metadata.compatible_os,
                       metadata.environment
                       ] + metadata.programming_languages,
          url=metadata.project_url,
          download_url=metadata.download_url,
          author=metadata.author_name,
          author_email=metadata.author_email,
          license=metadata.license_type,
          packages=find_packages(),
          install_requires=metadata.dependencies,
          dependency_links=[],
          test_suite='nose.collector',
          tests_require=['nose'],
          scripts=find_scripts(),
          zip_safe=False)
