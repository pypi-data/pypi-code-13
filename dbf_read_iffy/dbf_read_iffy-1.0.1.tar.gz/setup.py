def read_md(f):   # as long PyPI doesn't support README.md
    try:
        from pypandoc import convert      # need (apt)pandoc + (pip)pypandoc
        return convert(f, 'rst', 'md')
    except ImportError:
        return open(f, 'r').read()

try:
    from setuptools import setup
    st = True
except ImportError:
    from distutils.core import setup
    st = False

if st:
    try:
        from setuptools.command.build_py import build_py_2to3 as build_py
    except ImportError:
        from setuptools.command.build_py import build_py
else:
    try:
        from distutils.command.build_py import build_py_2to3 as build_py
    except ImportError:
        from distutils.command.build_py import build_py

setup(
  cmdclass={'build_py': build_py},
  name='dbf_read_iffy',
  py_modules=['dbf_read_iffy'],
  version='1.0.1',
  description="Read from dbf's if codepage is unsupported by modules dbf and codecs (895 cz Kamenicky, ..).",
  long_description=read_md('README.md'),
  install_requires=['dbf'],
  author='Mirek Zvolsky',
  author_email='zvolsky@seznam.cz',
  url='https://github.com/zvolsky/dbf_read_iffy',
  download_url='https://github.com/zvolsky/dbf_read_iffy/tarball/1.0',
  keywords=['dbf', 'dbase', 'foxpro', 'vfp', 'encoding', '895', 'Kamenicky', '620', 'Mazovia'],
  classifiers=[
      'Development Status :: 4 - Beta',
      'Intended Audience :: Developers',
      'Intended Audience :: Information Technology',
      'License :: OSI Approved :: MIT License',
      'Operating System :: OS Independent',
      'Topic :: Database',
      'Topic :: Database :: Database Engines/Servers',
      'Topic :: Software Development',
      'Programming Language :: Python',
      'Programming Language :: Python :: 2',
      'Programming Language :: Python :: 3',
  ],
)
