# coding=utf-8
from setuptools import setup, find_packages

version = {}
with open('./version.py') as fp:
    exec (fp.read(), version)

with open('./README.rst') as fp:
    readme = fp.read().strip()

setup(
    name='Flask-Arangodb',
    version=version['VERSION'],
    license='MIT',
    url='https://github.com/sebastiancodes/Flask-Arangodb',
    description='Flask extension for ArangoDB using python-arango',
    long_description=readme,
    author='Bas van den Broek',
    author_email='cwasvandenbroek@gmail.com',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'requests',
        'six',
        'python-arango',
        'flask'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
