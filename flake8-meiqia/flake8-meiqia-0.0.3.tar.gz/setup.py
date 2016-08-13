import re

from setuptools import setup


def get_version():
    content = open('flake8_meiqia/core.py').read()
    if isinstance(content, bytes):
        content = content.decode('utf-8')
    return re.search(r"""^__version__ = (['"])([^'"]+)\1""", content).group(2)


def get_long_description():
    with open('README.rst') as f:
        return f.read()


setup(
    name='flake8-meiqia',
    version=get_version(),
    author='Meiqia Developers',
    author_email='dev@meiqia.com',
    description='Python style guideline in Meiqia',
    long_description=get_long_description(),
    license='Apache License 2.0',
    url='https://github.com/Meiqia/flake8-meiqia',
    packages=[
        'flake8_meiqia',
        'flake8_meiqia.checks',
    ],
    classifier=[
        'Framework :: Flake8',
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Quality Assurance',
    ],
    install_requires=[
        'flake8'
    ],
    entry_points={
        'flake8.extension': [
            'MQ101 = flake8_meiqia.checks.comments:meiqia_todo_format',
            'MQ201 = flake8_meiqia.checks.excepts:meiqia_except_format',
            'MQ903 = flake8_meiqia.checks.other:meiqia_no_cr',
        ]
    },
)
