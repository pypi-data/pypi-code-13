from distutils.core import setup
import os

setup(
    name = 'rHLDS',
    packages = ['rHLDS'],
    version = '0.1.2',
    description = 'This library allows you to use Half-Life RCON protocol',
    long_description=open('README.md').read(),
    author = 'chmod',
    author_email = 'root@chmod.ga',
    url = 'https://github.com/chmod1/rHLDS.git',
    keywords = ['HLDS', 'RCON', 'Half-Life', 'hl', 'Counter-Strike', 'cstrike', 'cs'],
    license='MIT'
)
