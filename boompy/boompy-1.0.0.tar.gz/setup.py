from os import path
from setuptools import setup

from boom import __version__

long_description = open(
    path.join(
        path.dirname(__file__),
        'README.rst'
    )
).read()

entry_points = {
    'console_scripts': ['boom = boom:main']
}

setup(
    name='boompy',
    py_modules=['boom'],
    entry_points=entry_points,
    version=__version__,
    description="Simple command line snippets.",
    long_description=long_description,
    author='Bill Israel',
    author_email='bill.israel@gmail.com',
    url='https://github.com/epochblue/boom',
    keywords=['clipboard', 'boom', 'copy', 'paste'],
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
)

