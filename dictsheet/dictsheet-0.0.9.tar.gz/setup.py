from setuptools import setup, find_packages
from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]
# REFERENCE:
# http://stackoverflow.com/questions/14399534/how-can-i-reference-requirements-txt-for-the-install-requires-kwarg-in-setuptool

setup(
    name = 'dictsheet',
    version = '0.0.9',
    keywords = ('dictsheet', 'spreadsheet', 'gspread'),
    description = 'Dict wrapper for google spreadsheet',
    license = 'MIT License',
    install_requires = reqs,
    data_files = ['requirements.txt', 'README.md', 'LICENSE.txt'],
    url = 'https://github.com/previa/dictsheet',

    author = 'Chandler Huang, Xander Li',
    author_email = 'previa@gmail.com',
    
    packages = find_packages(),
    platforms = 'any',
)
