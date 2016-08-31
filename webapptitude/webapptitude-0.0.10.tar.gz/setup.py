
import re
import os
from setuptools import setup, find_packages
from pip.req import parse_requirements


def read(fname):
    """Simple shortcut for loading file content."""
    return open(os.path.join(os.path.dirname(__file__), fname), 'r').read()


def extract_version(content):
    """
    Extract the version identifier from a file's content.

    Examples supported:
        version = "0.0.0a1"
        __version__ = "1.2.3"
    """
    expr = re.compile(r'((?:__)?)version(\1)\s*=\s*'
                      r'(["\'])(\d+\.\d+\.\d+(?:[abc]\d*)?)\3')

    result = None
    for line in content.splitlines():
        result = expr.match(line.strip())
        if result is not None:
            break

    assert (result is not None), \
        "Failed to match a version string." % (content)
    return (result and result.group(4))


dependencies = parse_requirements('requirements.txt', session=False)

url = 'https://gitlab.com/samba/webapptitude'

# Retrieve module version from micro-module.
version = extract_version(read('webapptitude/version.py'))

if __name__ == '__main__':
    setup(
        name='webapptitude',
        version=version,

        author='Sam Briesemeister',
        author_email='sam.briesemeister+opensource@gmail.com',

        keywords='webapp2 google appengine',
        description=('A simple extension on webapp2 to accelerate development '
                     'on Google AppEngine'),

        license='BSD',
        url=url,
        download_url=('%s/repository/archive.tar.gz?ref=v%s' % (url, version)),

        entry_points=dict(
            console_scripts=[
                'gae_testrunner.py = webapptitude.test:main',
                'webapptitude_test = webapptitude.test:main'
            ]
        ),

        packages=['webapptitude'],
        install_requires=[str(ir.req) for ir in dependencies],
        zip_safe=True
    )
