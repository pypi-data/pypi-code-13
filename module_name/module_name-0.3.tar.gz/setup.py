from distutils.core import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except ImportError:
    long_description = open('README.md').read()

DISTNAME='module_name'
FULLVERSION='0.3'

setup(
    name = DISTNAME,
    packages = [DISTNAME],
    version = FULLVERSION,
    description = 'Simple Module to resolve module namespace',
    long_description = long_description,
    author = 'Dale Jung',
    author_email = 'dale@dalejung.com',
    url = 'https://github.com/dalejung/module_name',
    license = 'MIT',
    download_url = 'https://github.com/dalejung/module_name/tarball/'+FULLVERSION,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
