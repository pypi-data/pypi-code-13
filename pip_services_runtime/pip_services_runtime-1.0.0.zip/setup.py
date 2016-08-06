"""
Pip.Services Runtime
--------------------

Pip.Services is an open-source library of basic microservices.
Runtime represents a foundation the microservices are built on.

Links
`````

* `website <http://www.pipservices.org>`_
* `development version <http://github.com/pip-services/pip-services-runtime-python>`

"""

from setuptools import setup
from setuptools import find_packages

setup(
    name='pip_services_runtime',
    version='1.0.0',
    url='http://github.com/pip-services/pip-services-runtime-python',
    license='MIT',
    author='Digital Living Software Corp.',
    description='Microservices runtime framework for Pip.Services in Python',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    install_requires=[
        'iso8601', 'PyYAML', 'pymongo', 'bottle', 'requests'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]    
)
