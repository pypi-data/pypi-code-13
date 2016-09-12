from setuptools import setup
from pip.req import parse_requirements


def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='buku',
    version='0.0.2',
    description='Powerful command-line bookmark manager. Your mini web!',
    long_description=readme(),
    url='https://github.com/jarun/Buku',
    author='Ovv',
    author_email='ovv@outlook.com',
    license='GPLv3',
    packages=['buku', 'tests', 'auto-completion'],
    zip_safe=False,
    include_package_data=True,
    package_data = {'tests': ['ci-test-wrapper'],
        'auto-completion': ['bash/*', 'fish/*', 'zsh/*']},
    install_requires=['beautifulsoup4>=4.4.1', 'cryptography>=1.3.2'],
)