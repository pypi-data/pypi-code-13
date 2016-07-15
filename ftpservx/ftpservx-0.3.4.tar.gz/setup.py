#from distutils.core import setup
from setuptools import setup
from ftpservx import __version__ as VERSION
PACKAGE = "ftpservx"
NAME = "ftpservx"
DESCRIPTION = "ftpservx - Fast to run and cross-platform FTP-server. Based on PySide or PyQt4 and pyftpdlib. Licensed by GPL3."
LONG_DESCRIPTION = '''ftpservx - Fast to run and cross-platform FTP-server. Based on PySide or PyQt4 and pyftpdlib. Licensed by GPL3. Licensed by GPL3.'''
AUTHOR = "1_0"
AUTHOR_EMAIL = "1_0@usa.com"
URL = r"https://github.com/1-0/ftpservx"

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="GPL3",
    url=r'https://github.com/1-0/ftpservx',
    install_requires = ['PySide>=1.2', 'pyftpdlib>=1.5'],
    scripts = [r'./ftpservx.py',],
    #packages=[PACKAGE,],
    #packages=find_packages(exclude=["tests.*", "tests"]),
    #package_data=find_package_data(
#			PACKAGE,
#			only_in_packages=False
#	  ),
    extras_require={
    "PySide": ['PySide >= 1.0'],
    "pyftpdlib": ['pyftpdlib >= 1.5'],
},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: Developers",
        'Intended Audience :: End Users/Desktop',
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: System :: Networking",
    ],
    zip_safe=False,
)

