"""A compact GUI application for optical distortion calibration of endoscopes.

See:
https://github.com/gift-surg/endocal
"""

from setuptools import setup
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='endocal',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='16.07.22',

    description='A compact GUI application for optical distortion calibration of endoscopes',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/gift-surg/endocal',

    # Author details
    author='Dzhoshkun Ismail Shakir',
    author_email='d.shakir@ucl.ac.uk',

    # Choose your license
    license='BSD-3-Clause',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Intended Audience :: Healthcare Industry',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: Scientific/Engineering :: Image Recognition',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: BSD License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',

        # Currently tested only on Ubuntu 14.04 LTS
        'Operating System :: POSIX :: Linux',
    ],

    # What does your project relate to?
    keywords='optical distortion calibration, endoscope, endoscopy, medical imaging,'
             'image processing, biomedical engineering, medical physics,'
             'image-guided interventions',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['endocal', 'cad'],

    # As recommended in
    # https://docs.python.org/2/distutils/setupscript.html#installing-package-data
    package_dir={'endocal': 'endocal', 'cad': 'cad'},

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['PyYAML', 'numpy'],

    # External dependencies not on PyPI
    dependency_links=['http://opencv.org/'],

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={'endocal': ['data/sample_001/*'],
                  'cad': ['data/dxf/header.dxf', 'data/dxf/footer.dxf',
                          'data/dxf/polyline.dxf', 'data/dxf/seqend.dxf']},

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'endocal=endocal:main',
            'endocal-test=endocal:test',
            'dxf=cad:generate_dxf'
        ],
    },
)
