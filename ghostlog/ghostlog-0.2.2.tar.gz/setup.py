from setuptools import setup

setup(
    name = 'ghostlog',
    packages = [
        'ghostlog',
    ],
    version = '0.2.2',
    description = 'Easily log to syslog or stdout.',

    install_requires=[],
    tests_require=['testfixtures'],

    test_suite = 'tests.unit',

    author = 'Ezequiel Pochiero',
    author_email = 'ezequiel@spect.ro',

    url = 'https://bitbucket.org/spctr/spectro-ghostlog',
    download_url = 'https://bitbucket.org/spctr/spectro-ghostlog/get/v0.2.2.zip',

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
