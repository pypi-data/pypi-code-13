# lfi_url_encoding setup.py

from distutils.core import setup

setup(
    name = 'lfi_url_encoding',
    py_modules = ['lfi_url_encoding'],
    version = '1.0',
    description = 'A tool to encode URLs for LFI vulnerability.',
    author = 'Alexandre ZANNI',
    author_email = 'alexandre.zanni@openmailbox.org',
    maintainer = 'Alexandre ZANNI',
    url = 'https://github.com/noraj1337/CTF-tools/tree/master/Web/lfi_url_encoding',
    license = 'GNU General Public License v3.0',
    keywords = ["encoding", "LFI", "URL"],
    classifiers = [
        "Topic :: Security",
        "Environment :: Other Environment",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"
        ]
  )
