#!/usr/bin/python3


from setuptools import setup

setup(
    name='wayround_org_toxcorebot',
    version='0.1',
    author='Alexey Gorshkov',
    author_email='animus@wayround.org',
    url='https://github.com/AnimusPEXUS/wayround_org_toxcorebot',
    description='Tox chat bot based on wayround_org_toxcorebind',
    packages=[
        'wayround_org.toxcorebot'
        ],
    install_requires=[
        'wayround_org_utils',
        'wayround_org_toxcorebind'
        ],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX',
        ]
    )
