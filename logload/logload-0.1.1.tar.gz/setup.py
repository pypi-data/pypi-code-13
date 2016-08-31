
from setuptools import setup, find_packages

from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='logload',
    version='0.1.1',
    description='A syslog network load generator.',
    long_description=long_description,
    url='https://github.com/ofosos/logload/',
    author='Mark Meyer',
    author_email='mark@ofosos.org',
    license='GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Topic :: System :: Logging',
        'Topic :: Software Development :: Testing :: Traffic Generation',
    ],
    keywords='network syslog testing load',
    packages=find_packages(exclude=['test', 'docs', 'contrib']),
    install_requires=['funcparserlib'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'logload=logload.logload:main'
        ],
    },
    test_suite="test",
)
