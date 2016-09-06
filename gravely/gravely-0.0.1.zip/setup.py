"""A setuptools based setup module for gravely"""

from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext
from setuptools.extension import Extension


class numpy_aware_build_ext(build_ext):
    def finalize_options(self):
        '''
        Importing numpy deep down here serves two purposes:
        1. include_dirs=[numpy.get_include()] can be omitted
        2. setup.py stops depending on numpy to run
        '''
        build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        __builtins__.__NUMPY_SETUP__ = False
        import numpy
        self.include_dirs.append(numpy.get_include())


setup(
    name='gravely',
    version='0.0.1',
    python_requires='>=3.4',
    install_requires=[
        'h5py>=2.2',
        'numpy>=1.8.2',
    ],
    tests_require=[
        'nose>=1.0',
        'cython>=0.21',
    ],
    test_suite='nose.collector',
    extras_require = {
        'test':  ['nose>=1.0'],
        'diagnostics': ['matplotlib>=1.4'],
    },
    setup_requires=[
        'cython>=0.21',
        'setuptools>=20',
        'numpy>=1.8.2',
    ],
    ext_modules=[
        Extension('gravely.body', ['gravely/body.pyx']),
        Extension('gravely.solver', ['gravely/solver.pyx']),
    ],
    cmdclass={'build_ext': numpy_aware_build_ext},
    description=('A gravity simulator'
                 'written to taste modern Python packaging practices.'),
    url='https://lcode.info/mainline/gravely',
    author='LCODE team',
    author_email='team@lcode.info',
    license='LGPL v3.0',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Cython',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Physics',
    ],
    keywords='cython gravity physics simulation',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'gravely = gravely.main:main'
        ]
    },
)
