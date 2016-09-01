# coding=utf-8

from setuptools import setup


setup(
    name='versiontracker',
    version='1.0.3.20160901',
    description=u"Web scrapping software to keep track of the latest stable "
                u"version of several pieces of software.",
    url='https://gitlab.com/gallaecio/versiontracker',
    author=u"Adrián Chaves (Gallaecio)",
    author_email='adriyetichaves@gmail.com',
    license='AGPLv3+',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or '
            'later (AGPLv3+)',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Archiving :: Packaging',
    ],
    packages=['versiontracker'],
    install_requires=[
        'beautifulsoup4',
        'future',
        'python-dateutil',
        'requests',
        'termcolor',
    ],
    package_data={
        'versiontracker': ['data.json'],
    },
    entry_points={
          'console_scripts': [
              'versiontracker = versiontracker.__main__:main'
          ]
      },
)
