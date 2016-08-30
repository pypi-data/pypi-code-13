from setuptools import setup, find_packages


setup(
    name='cmsync',
    version='0.7',
    author='Wilson Santos',
    author_email='wilson@codeminus.org',
    description='A simple module to sync local folders that can run commands after the transfer.',

    license='Apache License 2.0',
    keywords='codeminus sync transfer',
    url='https://github.com/codeminus/cmsync',
    packages=find_packages(),
    scripts=[
        'bin/cmsync'
    ],
    install_requires=[
        'colorama'
    ]
)