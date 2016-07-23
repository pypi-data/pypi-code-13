from setuptools import setup
from setuptools.command.install import install
from setuptools.command.build_py import build_py
from setuptools.command.build_ext import build_ext
#
import scripts


class Pydart2BuildPy(build_py):
    def run(self):
        print("[pydart2] pre-build_py")
        build_py.run(self)
        print("[pydart2] post-build_py")


class Pydart2BuildExt(build_ext):
    def run(self):
        print("[pydart2] pre-build_ext")
        build_ext.run(self)
        print("[pydart2] post-build_ext")


class Pydart2Install(install):
    def run(self):
        print("[pydart2] pre-install")
        scripts.install_dart.clone()
        install.run(self)
        print("[pydart2] post-install")


setup(name='pydart2',
      version='0.3.1.2',
      description='Python Interface for DART Simulator',
      classifiers=[
          'Development Status :: 1 - Planning',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 2.7',
          'Topic :: Games/Entertainment :: Simulation'
      ],
      url='https://github.com/sehoonha/pydart2',
      author='Sehoon Ha',
      author_email='sehoon.ha@gmail.com',
      license='BSD',
      cmdclass={'build_py': Pydart2BuildPy,
                'build_ext': Pydart2BuildExt,
                'install': Pydart2Install, },
      packages=['pydart2'],
      zip_safe=False,
      include_package_data=True, )
