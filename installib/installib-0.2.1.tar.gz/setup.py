import sys
import os
import subprocess

from setuptools import setup, find_packages
from setuptools.command.install import install

EXCLUDE_FROM_PACKAGES = []

REQUIRES = []


PYWIN_32_EXE = {
    ((2, 5), False): "https://sourceforge.net/projects/pywin32/files/pywin32/Build%20220/pywin32-220.win32-py2.5.exe/download",
    ((2, 6), False): "https://sourceforge.net/projects/pywin32/files/pywin32/Build%20220/pywin32-220.win32-py2.6.exe/download",
    ((2, 7), False): "https://sourceforge.net/projects/pywin32/files/pywin32/Build%20220/pywin32-220.win32-py2.7.exe/download",
    ((3, 1), False): "https://sourceforge.net/projects/pywin32/files/pywin32/Build%20220/pywin32-220.win32-py3.1.exe/download",
    ((3, 2), False): "https://sourceforge.net/projects/pywin32/files/pywin32/Build%20220/pywin32-220.win32-py3.2.exe/download",
    ((3, 3), False): "https://sourceforge.net/projects/pywin32/files/pywin32/Build%20220/pywin32-220.win32-py3.3.exe/download",
    ((3, 4), False): "https://sourceforge.net/projects/pywin32/files/pywin32/Build%20220/pywin32-220.win32-py3.4.exe/download",
    ((3, 5), False): "https://sourceforge.net/projects/pywin32/files/pywin32/Build%20220/pywin32-220.win32-py3.5.exe/download",
    ((3, 6), False): "https://sourceforge.net/projects/pywin32/files/pywin32/Build%20220/pywin32-220.win32-py3.6.exe/download",
    ((2, 6), True): "https://sourceforge.net/projects/pywin32/files/pywin32/Build%20220/pywin32-220.win-amd64-py2.6.exe/download",
    ((2, 7), True): "https://sourceforge.net/projects/pywin32/files/pywin32/Build%20220/pywin32-220.win-amd64-py2.7.exe/download",
    ((3, 1), True): "https://sourceforge.net/projects/pywin32/files/pywin32/Build%20220/pywin32-220.win-amd64-py3.1.exe/download",
    ((3, 2), True): "https://sourceforge.net/projects/pywin32/files/pywin32/Build%20220/pywin32-220.win-amd64-py3.2.exe/download",
    ((3, 3), True): "https://sourceforge.net/projects/pywin32/files/pywin32/Build%20220/pywin32-220.win-amd64-py3.3.exe/download",
    ((3, 4), True): "https://sourceforge.net/projects/pywin32/files/pywin32/Build%20220/pywin32-220.win-amd64-py3.4.exe/download",
    ((3, 5), True): "https://sourceforge.net/projects/pywin32/files/pywin32/Build%20220/pywin32-220.win-amd64-py3.5.exe/download",
    ((3, 6), True): "https://sourceforge.net/projects/pywin32/files/pywin32/Build%20220/pywin32-220.win-amd64-py3.6.exe/download",
}


def install_pywin32():
    is_64bits = sys.maxsize > 2 ** 32
    with open(os.devnull, "w") as devnull:
        process = subprocess.Popen(
            ["easy_install", PYWIN_32_EXE[(sys.version_info[0:2], is_64bits)]],
            stdin=subprocess.PIPE,
            stderr=devnull)
        process.wait()


class MyInstall(install):
    def run(self):
        install_pywin32()
        install.run(self)


setup(
    name='installib',
    version='0.2.1',
    description='Install helper library',
    author='Ivan Martin',
    author_email='ivanprjcts@gmail.com',
    url='https://github.com/ivanprjcts/installib',
    install_requires=REQUIRES,
    license='BSD',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    zip_safe=False,
    cmdclass={'install': MyInstall}
)
