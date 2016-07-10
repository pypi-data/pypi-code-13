#!/usr/bin/python3

import glob

from setuptools import setup, Extension
#from Cython.Build import cythonize
from Cython.Distutils import build_ext


import wayround_org.utils.cython
import wayround_org.utils.pkgconfig

cflags = wayround_org.utils.pkgconfig.pkgconfig('libtoxcore', ['--cflags'])
ldflags = wayround_org.utils.pkgconfig.pkgconfig('libtoxcore', ['--libs'])

if cflags is None or ldflags is None:
    raise Exception(
        "can't determine `libtoxcore' compilation and linking parameters"
        " using pkg-config"
        )

if isinstance(cflags, str):
    cflags = cflags.split()

if isinstance(ldflags, str):
    ldflags = ldflags.split()

include_dirs = wayround_org.utils.pkgconfig.pkgconfig_include(
    'libtoxcore',
    remove_Is=True
    )

libs = wayround_org.utils.pkgconfig.pkgconfig_libs(
    'libtoxcore',
    remove_ls=True
    )

if isinstance(include_dirs, str):
    include_dirs = include_dirs.split()

if isinstance(libs, str):
    libs = libs.split()

extensions = [
    Extension(
        "wayround_org.toxcorebind.tox",
        ["wayround_org/toxcorebind/tox.pyx"],
        # libraries=libs,
        # include_dirs=include_dirs,
        extra_compile_args=cflags,
        extra_link_args=ldflags
        )
    ]

wayround_org.utils.cython.cythonize(
    glob.glob('wayround_org/toxcorebind/*.pyx'),
    cython_options=['-3']
    )

setup(
    name='wayround_org_toxcorebind',
    version='0.2.3',
    author='Alexey Gorshkov',
    author_email='animus@wayround.org',
    url='https://github.com/AnimusPEXUS/wayround_org_toxcorebind',
    description='Python toxcore binding',
    packages=[
        'wayround_org.toxcorebind'
        ],
    install_requires=[
        'Cython',
        'wayround_org_utils',
        ],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX',
        ],
    ext_modules=extensions, #cythonize(extensions),
    cmdclass={'build_ext': build_ext},
    package_data={'wayround_org.toxcorebind': ['*.pxd']},
    )
