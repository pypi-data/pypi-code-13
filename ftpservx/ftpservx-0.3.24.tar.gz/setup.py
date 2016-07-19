#from distutils.core import setup
from setuptools import setup
from ftpservx.main import __version__ as VERSION
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
    keywords='FTP-server, pyside, pyqt4',
    license="GPL3",
    url=r'https://github.com/1-0/ftpservx',
    install_requires = ['PySide', 'pyftpdlib'],
#    scripts = [r'ftpservx.py',],
    py_modules=['pyside', 'pyftpdlib'],
#    namespace_packages=['ftpservx',],
    packages=['ftpservx',],
    #packages=[PACKAGE,],
    #packages=find_packages(exclude=["tests.*", "tests"]),
    #package_data=find_package_data(
#           PACKAGE,
#           only_in_packages=False
#     ),
    #extras_require={
    #"PySide": ['PySide>=1.0'],
    #"pyftpdlib": ['pyftpdlib>=1.5'],
#},
    #entry_points={
        #'console_scripts': [
            #'ftpservx = ftpservx.py:_main',
        #],
#},
    entry_points={
        'console_scripts': [
            'ftpservx = ftpservx.main:main'
        ]
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

