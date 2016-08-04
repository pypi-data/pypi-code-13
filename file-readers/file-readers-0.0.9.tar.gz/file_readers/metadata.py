NAME = 'file-readers'
VERSION = '0.0.9'
DESCRIPTION = 'Library of different types of file reader and data collector classes.'
URL = 'https://github.com/mjalas/file-readers'
AUTHOR = 'Mats Jalas'
AUTHOR_EMAIL = 'mats.jalas@gmail.com'
LICENSE = 'MIT'
# See https://PyPI.python.org/PyPI?%3Aaction=list_classifiers
classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.5',
]
exclude = ['csv/tests', 'excel/tests']
setup_requires = ['nose>=1.0', 'coverage>=4.0.3', 'openpyxl>=2.3.4']
test_suite = 'nose.collector'
tests_require = ['nose']
install_requires = ['openpyxl']
