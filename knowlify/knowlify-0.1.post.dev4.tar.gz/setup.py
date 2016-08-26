from setuptools import setup, find_packages
from os.path import (
    abspath,
    dirname,
    join,
)
from operator import lt, gt, eq, le, ge
import sys
import versioneer



SYS_VERSION = '.'.join(list(map(str, sys.version_info[:3])))

STR_TO_CMP = {
    '<': lt,
    '<=': le,
    '=': eq,
    '==': eq,
    '>': gt,
    '>=': ge,
}


def _filter_requirements(lines_iter):
    for line in lines_iter:
        line = line.strip()
        if not line or line.startswith('#'):
            continue



        yield line


def read_requirements(path):
    """
    Read a requirements.txt file, expressed as a path relative to Zipline root.
    Returns requirements with the pinned versions as lower bounds
    """
    real_path = join(dirname(abspath(__file__)), path)
    with open(real_path) as f:
        reqs = _filter_requirements(f.readlines())

        return list(reqs)


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='knowlify',
    description='Add context dependent information to a html file',
    long_description=readme,
    author='Lotanna Ezenwa',
    author_email='lota.ezenwa@gmail.com',
    url='https://github.com/LotannaEzenwa/knowlify',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    test_suite='nose.collector',
    tests_require=['nose'],
    scripts=['bin/knowl_setup.sh'],
    install_requires=read_requirements('requirements.txt'),
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
)