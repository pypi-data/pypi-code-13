# coding=utf-8

import os.path
from setuptools import setup

_folder_path = os.path.dirname(__file__)
_version_path = os.path.join(_folder_path, 'versiontracker', '_version.py')
with open(_version_path) as f:
    exec(f.read())
version = __version__
git_url = 'https://gitlab.com/gallaecio/versiontracker'
with open(os.path.join(_folder_path, 'requirements.txt')) as f:
    requirements = f.read().splitlines()

setup(
    name='versiontracker',
    version=version,
    description=u"Web scrapping software to keep track of the latest stable "
                u"version of several pieces of software.",
    url='http://version-tracker.rtfd.io/',
    download_url='{}/repository/archive.tar.gz?ref=v{}'.format(
        git_url, version),
    author=u"Adrián Chaves (Gallaecio)",
    author_email='adriyetichaves@gmail.com',
    license='AGPLv3+',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or '
            'later (AGPLv3+)',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Archiving :: Packaging',
    ],
    packages=['versiontracker'],
    install_requires=requirements,
    package_data={
        'versiontracker': ['data.json'],
    },
    entry_points={
          'console_scripts': [
              'versiontracker = versiontracker.__main__:main'
          ]
      },
)
