
import os
import re

# try:
#     from semantic_release import setup_hook
#     setup_hook(sys.argv)
# except ImportError as e:
#     print e

try:
    import setuptools
except ImportError:
    import distutils.core
    setup = distutils.core.setup
else:
    setup = setuptools.setup


def _get_version():
    path = os.path.join(PATH_TO_FILE, 'ptestpypi', '__init__.py')
    version_re = r".*__version__ = '(.*?)'"
    fo = open(path)
    try:
        return re.compile(version_re, re.S).match(fo.read()).group(1)
    finally:
        fo.close()


def _get_long_description():
    path = os.path.join(PATH_TO_FILE, 'README.md')
    fo = open(path)
    try:
        return fo.read()
    finally:
        fo.close()


def parse_requirements(file_name):
    requirements = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'(\s*#)|(\s*$)', line):
            continue
        if re.match(r'\s*-e\s+', line):
            requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1', line))
        elif re.match(r'\s*-f\s+', line):
            pass
        else:
            requirements.append(line)

    return requirements


def parse_dependency_links(file_name):
    dependency_links = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'\s*-[ef]\s+', line):
            dependency_links.append(re.sub(r'\s*-[ef]\s+', '', line))

    return dependency_links


PATH_TO_FILE = os.path.dirname(__file__)
VERSION = _get_version()
LONG_DESCRIPTION = _get_long_description()

setup(
    name='ptestpypi',
    version=VERSION,
    url='https://ptestpypi.com/',
    license='MIT License',
    author='ptestpypi',
    author_email='dev@ptestpypi.com',
    description='Payments API',
    long_description=LONG_DESCRIPTION,
    packages=['ptestpypi'],
    test_suite='nose.collector',
    install_requires=parse_requirements('requirements.txt'),
    tests_require=parse_requirements('test-requirements.txt'),
    dependency_links=parse_dependency_links('requirements.txt'),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
