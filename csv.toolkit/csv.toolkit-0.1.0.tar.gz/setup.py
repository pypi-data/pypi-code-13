#
# Copyright (c) 2016, Michael Conroy
#


from setuptools import setup, find_packages


setup(
    name='csv.toolkit',
    version='0.1.0',
    description='Tools for working with CSV files',
    long_description=open('README.rst', 'r').read(),
    keywords='csv tool validation processing',
    author='Michael Conroy',
    author_email='sietekk@gmail.com',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    url='https://github.com/sietekk/csv.toolkit',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    zip_safe=True,
    include_package_data=True,
    namespace_packages=['csv'],
    entry_points={
        'console_scripts': [
            'csvtoolkit = csv.toolkit.scripts:main',
        ]
    },
    install_requires=[
        'six>=1.5,<2',
    ],
    extras_require={
        'dev': [
            'pbbt>=0.1.4,<1',
            'coverage>=3.7,<4',
            'nose>=1.3,<2',
            'nosy>=1.1,<2',
            'prospector[with_pyroma]>=0.12,<0.13',
            'twine>=1.5,<2',
            'wheel>=0.24,<0.25',
            'Sphinx>=1.3,<2',
            'sphinx-autobuild>=0.5,<0.6',
            'tox>=2,<3',
            'flake8>=2.5.0,<3',
        ],
    },
    test_suite='nose.collector',
)


