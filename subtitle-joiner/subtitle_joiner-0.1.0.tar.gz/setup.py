
import sys

from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

import joiner

install_requires = [
    'Pillow>=3.3.0'
]

# Conditional dependencies:

# sdist
if 'bdist_wheel' not in sys.argv:
    try:
        # noinspection PyUnresolvedReferences
        import argparse
    except ImportError:
        install_requires.append('argparse>=1.2.1')


# bdist_wheel
extra_requires = {
    # http://wheel.readthedocs.io/en/latest/#defining-conditional-dependencies
    ':python_version == "2.6"'
    ' or python_version == "3.0"'
    ' or python_version == "3.1" ': ['argparse>=1.2.1']
}

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='subtitle_joiner',
    version=joiner.__version__,
    description='An image merge tool for movie screenshots',
    long_description=long_description,
    url='https://github.com/TreyCai/SubtitleJoiner/issues',
    download_url='https://github.com/TreyCai/SubtitleJoiner/issues',
    author=joiner.__author__,
    author_email='imtreywalker@gmail.com',
    license=joiner.__license__,
    packages=find_packages(),
    package_data={},
    data_files=[],
    entry_points={
        'console_scripts': {
            'joiner = joiner.__main__.main'
        }
    },
    extras_require=extra_requires,
    install_requires=install_requires,
    classifiers=[
        # 3 - Alpha
        # 4 - Beta
        # 5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        # 'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Topic :: Terminals',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Utilities'
    ]
)
