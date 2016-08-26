'''Renders a graphical representation of the data provided'''

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='stegart',
    version='0.1.0',
    description='Renders a graphical representation of the data provided',
    long_description=long_description,
    url='https://github.com/kulinacs/stegart',
    author='kulinacs',
    author_email='nicklaus@kulinacs.com',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Multimedia :: Graphics',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='image representation steganography',
    packages=find_packages(),
    install_requires=['binascii', 'numpy', 'argparse'],
    entry_points={
        'console_scripts': [
            'stegart=stegart.stegart:main',
        ],
    },
)
