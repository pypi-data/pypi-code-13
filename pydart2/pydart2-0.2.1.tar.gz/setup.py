from setuptools import setup
from setuptools.command.install import install
from setuptools.command.build_py import build_py
from setuptools.command.build_ext import build_ext


class Pydart2Build(build_py):
    def run(self):
        print("[pydart2] pre-build")
        build_py.run(self)
        print("[pydart2] post-build")


class Pydart2BuildExt(build_ext):
    def run(self):
        print("[pydart2] pre-build_ext")
        build_ext.run(self)
        print("[pydart2] post-build_ext")


class Pydart2Install(install):
    def run(self):
        print("[pydart2] pre-install")
        install.run(self)
        print("[pydart2] post-install")

setup(name='pydart2',
      version='0.2.1',
      description='Python Interface for DART Simulator',
      url='https://github.com/sehoonha/pydart2',
      author='Sehoon Ha',
      author_email='sehoon.ha@gmail.com',
      license='BSD',
      cmdclass={'build_py': Pydart2Build,
                'build_ext': Pydart2BuildExt,
                'install': Pydart2Install},
      packages=['pydart2'],
      zip_safe=False)
