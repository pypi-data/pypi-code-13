from setuptools import setup

setup(
    name = 'ghostlog',
    packages = [
        'ghostlog',
    ],
    version = '0.1.0',
    description = 'Easily log to syslog or stdout.',

    install_requires=[],
    tests_require=['testfixtures'],

    test_suite = 'tests.unit',

    author = 'Ezequiel Pochiero',
    author_email = 'ezequiel@spect.ro',

    keywords = ['log', 'logging', 'syslog'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Logging',
        'Topic :: System :: Systems Administration'
    ]
)
