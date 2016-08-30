import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


requirements = [
    'Delorean==0.6.0',
]


setup(
    name='time_aware_polyline',
    packages=['time_aware_polyline'],
    version='0.1.0',
    description='Time aware encoded polyline for geospatial data',
    author='HyperTrack',
    author_email='devops@hypertrack.io',
    url='https://github.com/hypertrack/time-aware-polyline-py',
    license='MIT',
    download_url='https://github.com/hypertrack/time-aware-polyline-py/tarball/0.1',
    keywords=['geospatial', 'encoding', 'polyline'],
    classifiers=[],
)
