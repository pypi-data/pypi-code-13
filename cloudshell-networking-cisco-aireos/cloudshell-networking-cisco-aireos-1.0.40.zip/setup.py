from setuptools import setup, find_packages
import os

with open(os.path.join('version.txt')) as version_file:
    version_from_file = version_file.read().strip()

with open('requirements.txt') as f_required:
    required = f_required.read().splitlines()

with open('test_requirements.txt') as f_tests:
    required_for_tests = f_tests.read().splitlines()

setup(
    name='cloudshell-networking-cisco-aireos',
    url='https://github.com/QualiSystems/Cisco-AIREOS-Shell',
    author='Quali',
    license='Apache 2.0',
    author_email='info@quali.com',
    packages=find_packages(),
    install_requires=required,
    tests_require=required_for_tests,
    version=version_from_file,
    description='Cisco AireOS resource driver',
    include_package_data=True,
    keywords="sandbox cloud cmp cloudshell",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: Apache Software License",
    ],
    exclude_package_data={'': ['.gitignore', 'test']}
)
