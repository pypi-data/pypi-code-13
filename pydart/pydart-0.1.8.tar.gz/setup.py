# from setuptools import setup
# from setuptools.extension import Extension

from distutils.core import setup
from distutils.core import Extension

DIR = 'pydart/'
CXX_FLAGS = '-Wall -msse2 -fPIC -std=c++11 -Xlinker -rpath /usr/local/lib '
CXX_FLAGS += '-O3 -DNDEBUG '
CXX_FLAGS += '-g -fno-omit-frame-pointer -fno-inline-functions '
CXX_FLAGS += '-fno-inline-functions-called-once -fno-optimize-sibling-calls '
pydart_api = Extension('pydart_api',
                       define_macros=[('MAJOR_VERSION', '1'),
                                      ('MINOR_VERSION', '0')],
                       include_dirs=['/usr/local/include',
                                     '/usr/include/eigen3',
                                     '/usr/include/python2.7',
                                     '/usr/include/bullet' ],
                       libraries=['python2.7'],
                       library_dirs=['/usr/local/lib'],
                       extra_compile_args=CXX_FLAGS.split(),
                       swig_opts=['-c++'],
                       sources=[DIR + 'pydart_api.cpp',
                                DIR + 'pydart_api.i'],
                       depends=[DIR + 'pydart_api.h',
                                DIR + 'numpy.i'])


setup(name='pydart',
      version='0.1.8',
      description='Python Interface for DART Simulator',
      url='https://github.com/sehoonha/pydart',
      author='Sehoon Ha',
      author_email='sehoon.ha@gmail.com',
      license='BSD',
      packages=['pydart'],
      ext_modules=[pydart_api])
