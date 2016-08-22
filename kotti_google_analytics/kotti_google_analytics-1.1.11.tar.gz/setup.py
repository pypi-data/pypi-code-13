import os

from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
except IOError:
    README = ''
try:
    CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()
except IOError:
    CHANGES = ''

version = "1.1.11"

install_requires = [
    'Kotti>=1.0.0',
    'unidecode',
    'keyring',
    'oauth2client>=1.5',
    'google-api-python-client>=1.4.2',
    'python-dateutil',
    'addressable>=1.4.2',
    'inspect-it>=0.3.2',
    'werkzeug>=0.10',
    'keyring==5.3',
    'click>=3.3',
    'pyyaml>=3',
    'prettytable>=0.7',
    'colorama>=0.3',
    'googleanalytics>=0.22.2',
    'kotti_controlpanel>=1.0.0'
]


setup(
    name='kotti_google_analytics',
    version=version,
    description="Google Analytics for Kotti",
    long_description='\n\n'.join([README, CHANGES]),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "License :: Repoze Public License",
    ],
    author='Oshane Bailey',
    author_email='b4.oshany@gmail.com',
    url='https://github.com/b4oshany/kotti_google_analytics',
    keywords=('google analytics kotti web cms wcms pylons pyramid'
              'sqlalchemy bootstrap tracking users'),
    license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=[],
    dependency_links=[],
    entry_points={
        'fanstatic.libraries': [
            'kotti_google_analytics = kotti_google_analytics.fanstatic:library',
        ],
    },
    extras_require={},
)
