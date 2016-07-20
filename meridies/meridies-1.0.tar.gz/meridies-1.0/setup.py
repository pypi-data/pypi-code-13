from setuptools import setup

import glob

setup(
    name = 'meridies',
    version = '1.0',
    description = '',
    author = 'Fabian Peter Hammerle',
    author_email = 'fabian.hammerle@gmail.com',
    url = 'https://github.com/fphammerle/meridies',
    download_url = 'https://github.com/fphammerle/meridies/tarball/1.0',
    keywords = [],
    classifiers = [],
    scripts = glob.glob('scripts/*'),
    install_requires = ['pytz', 'python-dateutil'],
    tests_require = ['pytest']
    )
