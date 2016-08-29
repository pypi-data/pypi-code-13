from setuptools import setup, find_packages

VERSION = open('VERSION.txt').read().strip()
README = open('README.txt').read()
AUTHOR = 'Sven Rahmann'
EMAIL = 'Sven.Rahmann@gmail.com'
URL = 'https://bitbucket.org/svenrahmann/amplikyzer/'
LICENSE = 'MIT'

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'Natural Language :: English',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
]


setup(
    name='amplikyzer2',
    description='amplicon methylation analyzer for SFF (flowgrams) and FASTQ (MiSeq) files',
    # scripts=['bin/show-nonascii.py', 'bin/amplikyzer2', 'bin/amplikyzer2gui'],
    entry_points={
        'console_scripts': ['amplikyzer2 = amplikyzer2:main'],
        'gui_scripts': ['amplikyzer2gui = amplikyzer2:gui']
    },
    python_requires='>=3.4',
    install_requires=['geniegui >= 0.200', 'numpy >= 1.9.0', 'numba >= 0.26'],
    packages=find_packages(),
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    long_description=README,
    license=LICENSE,
    classifiers=CLASSIFIERS,
    zip_safe=False
)
