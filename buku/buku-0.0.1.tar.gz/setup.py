from setuptools import setup
from pip.req import parse_requirements


def readme():
    with open('README.md') as f:
        return f.read()

install_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='buku',
    version='0.0.1',
    description='Powerful command-line bookmark manager. Your mini web!',
    long_description=readme(),
    url='https://github.com/jarun/Buku',
    author='Ovv',
    author_email='ovv@outlook.com',
    license='GPLv3',
    packages=['buku'],
    zip_safe=False,
    install_requires=reqs,
    include_package_data=True,
)