# -*- coding: utf-8 -*-


import os
import setuptools
import distutils.log
from distutils.command.build_ext import build_ext
from distutils.errors import LinkError

import syskit


if syskit.platform != 'linux':
    from syskit import _bindings
    bindings = _bindings.Binding()  # XXX
    EXT_MODULES = [bindings.ffi.verifier.get_extension()]
else:
    EXT_MODULES = []


class BuildExtCommand(build_ext):
    """Extend the build_ext command

    On Solaris we need to compile the helper application sargs64.so.
    We compile this unconditionally even if the python is already a
    64-bit process, it simply won't be used in that case.
    """

    def run(self):
        build_ext.run(self)
        if syskit.platform == 'sunos':
            self.build_sargs64()

    def build_sargs64(self):
        """Build the sargs64.so helper for solaris"""
        src = os.path.join('syskit', 'sargs64.c')
        destdir = os.path.join(self.build_lib, 'syskit')
        try:
            self.compiler.link_executable([src],
                                          'sargs64.so',
                                          output_dir=destdir,
                                          extra_preargs=['-m64'])
        except LinkError:
            distutils.log.warn(
                'sargs64.so not built, this is normal on 32-bit platforms')


setuptools.setup(
    name='syskit',
    version=syskit.__version__,
    author='Floris Bruynooghe',
    author_email='flub@devork.be',
    license='MIT',
    url='http://bitbucket.org/flub/syskit',
    download_url='http://pypi.python.org/pypi/syskit',
    description='System information for pedants',
    packages=['syskit', 'syskit/_bindings'],
    zip_safe=False,
    ext_package='syskit',
    ext_modules=EXT_MODULES,
    install_requires=['cffi'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX :: SunOS/Solaris',
        'Programming Language :: C',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Operating System Kernels',
        'Topic :: System :: Systems Administration',
    ],
    cmdclass={'build_ext': BuildExtCommand},
)
