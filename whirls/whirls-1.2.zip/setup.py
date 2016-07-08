from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='whirls',
    version='1.2',
    description='A fullscreen program that displays an animated, twisting tessellation of whirls.',
    long_description=long_description,
    url='https://bitbucket.org/David_Nickerson/whirls',
    author='David Nickerson',
    author_email='UNKNOWN',
    license='GPLv3+',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Topic :: Games/Entertainment :: Simulation',
    ],
    keywords='curve derived polygon pursuit spiral whirl',
    package_dir={'': 'src'},
    py_modules=['whirls'],
    install_requires=['matplotlib', 'numpy', 'pgu', 'pygame', 'scipy'],
    entry_points={
        'console_scripts': [
            'whirls=whirls:main',
        ],
    },
)
