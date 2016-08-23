from setuptools import setup, find_packages

setup(
    name = 'dictsheet',
    version = '0.0.3',
    keywords = ('dictsheet', 'spreadsheet', 'gspread'),
    description = 'Dict wrapper for google spreadsheet',
    license = 'MIT License',
    install_requires = ['gspread>=0.4.1'],
    url = 'https://github.com/previa/dictsheet',

    author = 'Chandler Huang, Xander Li',
    author_email = 'previa@gmail.com',
    
    packages = find_packages(),
    platforms = 'any',
)
