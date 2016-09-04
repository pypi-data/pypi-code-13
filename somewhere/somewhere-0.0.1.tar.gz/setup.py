import setuptools
import somewhere

long_description = '''\
This is a GNU which replacement with the following features:
- it is portable (Windows, Linux);
- it understands PATHEXT on Windows;
- it can print <em>all</em> matches on the PATH;
- it can note "near misses" on the PATH (e.g. files that match but
  may not, say, have execute permissions; and
- it can be used as a Python module.
'''


setuptools.setup(
    name="somewhere",
    version=somewhere.__version__,

    author="Nick Timkovich",
    author_email="prometheus235@gmail.com",
    url="http://github.com/nicktimko/somewhere",
    license="MIT",

    packages=['somewhere'],
    description="Locates files like the Windows 'where' or the *nix 'which' utilities.",
    long_description=long_description,
    keywords=["which", "find", "path", "where"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],

    entry_points={
        'console_scripts': [
            'where = where:main',
        ]
    },
)
