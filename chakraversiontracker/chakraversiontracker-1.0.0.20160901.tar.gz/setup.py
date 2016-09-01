# coding=utf-8

from setuptools import setup


setup(
    name='chakraversiontracker',
    version='1.0.0.20160901',
    description=u"Software to detect packages in rolling repositories of "
                u"Chakra that are out of date.",
    url='https://gitlab.com/gallaecio/chakraversiontracker',
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
    packages=['chakraversiontracker'],
    install_requires=[
        'beautifulsoup4',
        'jinja2',
        'termcolor',
        'versiontracker',
    ],
    package_data={
        'chakraversiontracker': [
            'data.json',
            'templates/packages.cli',
            'templates/packages.txt',
            'templates/repositories.cli',
            'templates/repositories.txt',
        ],
    },
    entry_points={
          'console_scripts': [
              'chakraversiontracker = chakraversiontracker.__main__:main'
          ]
      },
)
