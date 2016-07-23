# vi:et:ts=4 sw=4 sts=4

import os
import sys

from setuptools import setup, find_packages

_DESC = """local-pipelines is a parser for bitbucket-pipelines.yml files that
will run the pipeline using your local docker-engine.
"""

from pipelines import __version__


def main():
    """ Creates our package """

    install_requires = []

    with open('requirements.txt') as ifp:
        for dependency in ifp.readlines():
            dependency = dependency.strip()

            if len(dependency) == 0 or dependency.startswith('#'):
                continue

            install_requires.append(dependency)

    setup(
        name='local-pipelines',
        version=__version__,
        description=_DESC,
        packages=find_packages('.'),
        install_requires=install_requires,
        zip_safe=True,
        author='Gary Kramlich',
        author_email='grim@reaperworld.com',
        url='http://bitbucket.org/rw_grim/local-pipelines',
        entry_points = {
            'console_scripts': ['pipelines=pipelines.core:main'],
        }
    )


if __name__ == '__main__':
    main()

