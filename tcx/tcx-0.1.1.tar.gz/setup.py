#!/usr/bin/env python
from setuptools import find_packages, setup
import versioneer


setup(
    name='tcx',
    version=versioneer.get_version(),
    description='TXC to GeoJson-like dict parser',
    url='http://github.com/cwygoda/tcx',
    author='Christian Wygoda',
    author_email='info@wygoda.net',
    license='MIT',
    packages=find_packages(),
    cmdclass=versioneer.get_cmdclass(),
    install_requires=[
        'iso8601'
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest',
    ],
    zip_safe=True,
    download_url='https://github.com/cwygoda/tcx/tarball/v0.1.1',
    keywords=[
        'tcx',
        'geojson'
    ],
)
