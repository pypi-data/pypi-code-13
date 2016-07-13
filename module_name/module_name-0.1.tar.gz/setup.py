from distutils.core import setup

DISTNAME='module_name'
FULLVERSION='0.1'

setup(
    name = DISTNAME,
    packages = [DISTNAME],
    version = FULLVERSION,
    description = 'Simple Module to resolve module namespace',
    author = 'Dale Jung',
    author_email = 'dale@dalejung.com',
    url = 'https://github.com/dalejung/module_name',
    download_url = 'https://github.com/dalejung/module_name/tarball/'+FULLVERSION,
    classifiers = [],
)
