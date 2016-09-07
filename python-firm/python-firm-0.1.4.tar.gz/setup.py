from os import environ
from distutils.core import setup
import gen.compile
import gen.subbuild

extra_arguments = dict(
    requires=[
        'cffi>=1.0.0',
        'pytest>=2.9.2'
    ],
    ext_modules=[gen.compile.ffi.distutils_extension()]
)

if 'NO' != environ.get('FIRM_USE_SETUPTOOLS', 'YES').upper():
    try:
        from setuptools import setup
    except ImportError:
        pass
    else:
        extra_arguments = dict(
            setup_requires=[
                'cffi>=1.0.0',
                'pytest>=2.9.2'
            ],
            cffi_modules=['gen/compile.py:ffi'],
            install_requires=['cffi>=1.0.0'],
        )


setup(
    name='python-firm',
    version='0.1.4',
    description='FIRM Optimising Compiler Backend',
    author='William ML Leslie',
    author_email='william.leslie.ttg@gmail.com',
    license='LGPL v2.1',
    url='https://bitbucket.org/william_ml_leslie/python-firm',
    packages=['firm', 'firm.tests'],
    cmdclass={'build-make' : gen.subbuild.build_make},
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Compilers',
        ],
    **extra_arguments
)
