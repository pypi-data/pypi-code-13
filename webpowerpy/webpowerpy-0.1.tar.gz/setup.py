from __future__ import print_function
from setuptools import setup, find_packages

setup(
    name='webpowerpy',
    version='0.1',
    url='http://github.com/dooplan/webpower/',
    license='GNU General Public License v3.0',
    author='Pasqual Guerrero',
    install_requires=['suds'],
    author_email='pasqual.guerrero@gmail.com',
    description='Python wrapper around WebPower SOAP-v4.2 API',
    packages=find_packages(),
    classifiers = [
        'Programming Language :: Python',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: Unix',
    ],
)