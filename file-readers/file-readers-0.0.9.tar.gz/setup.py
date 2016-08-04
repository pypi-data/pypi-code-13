from setuptools import setup, find_packages
from codecs import open
from os import path
import file_readers.metadata as metadata

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
long_description = ""

try:
    from pypandoc import convert
    if path.exists(path.join(here, 'README.md')):
        long_description = convert('README.md', 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")

setup(
    name=metadata.NAME,
    version=metadata.VERSION,
    description=metadata.DESCRIPTION,
    long_description=long_description,
    url=metadata.URL,
    author=metadata.AUTHOR,
    author_email=metadata.AUTHOR_EMAIL,
    license=metadata.LICENSE,
    classifiers=metadata.classifiers,
    packages=find_packages(exclude=metadata.exclude),
    setup_requires=metadata.setup_requires,
    test_suite=metadata.test_suite,
    tests_require=metadata.tests_require,
    install_requires=metadata.install_requires,
)
