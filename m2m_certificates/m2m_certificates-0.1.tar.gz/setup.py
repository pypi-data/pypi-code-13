"""Setup module for m2m_certificates.
"""

from setuptools import setup, find_packages
from codecs import open
from os import path
from pip.req import parse_requirements

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

install_reqs = parse_requirements("requirements.txt", session=False)
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name = 'm2m_certificates',
    version = 0.1,
    packages = find_packages(),
    license = 'AGPL',
    url = 'https://github.com/LoyVanBeek/m2m_certificates',
    download_url = 'https://github.com/LoyVanBeek/m2m_certificates/tarball/0.1',
    description = 'Python module for generating and parsing M2M format certificates',
    long_description = long_description,
    keywords = 'nfc ndef m2m',
    author = 'Loy van Beek',
    author_email = 'l.vanbeek@ultimaker.com',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Security :: Cryptography'
    ],

    install_requires = reqs,
)
