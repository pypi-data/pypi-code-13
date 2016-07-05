from setuptools import setup, find_packages

import picom

setup(name='picom',
      version=picom.__version__,
      description='Help communicating Iot with Raspberry Pi',
      url='https://github.com/Thumberd/PiCom',
      author='Jérémy Albrecht',
      author_email='ajeremyalbrecht@gmail.com',
      license='MIT',
      include_package_data=True,
      install_requires=['requests',],
      packages=find_packages()
      )
