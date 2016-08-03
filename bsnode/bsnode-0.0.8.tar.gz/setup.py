# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='bsnode',
    version='0.0.8',
    author='Konstantin Kruglov',
    author_email='kruglovk@gmail.com',
    description='empty',
    # long_description=bsnode.__long_description__,
    url='https://github.com/battleserver/bsnode',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'bs-node = bsnode:cli',
        ],
    },
    package_data={'bsnode': ['make/templates/*.tpl']},
    install_requires=[
        'bsstatusflags==0.2.0',
        'svdlib==0.0.2',
        'pyscfg==1.0.0',
        'Jinja2==2.8',
        'click==6.6',
        'svdlib==0.0.2'],
    license='Apache License Version 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: POSIX :: Linux',
    ],
)
