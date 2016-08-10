from distutils.core import setup
from sys import platform as _platform
import os

if _platform == "linux" or _platform == "linux2":
    os.system('patchelf --set-rpath "\$ORIGIN" --force-rpath phoxi/_phoPython2Linux.so')
    os.system('patchelf --set-rpath "\$ORIGIN" --force-rpath phoxi/_phoPython3Linux.so')

setup(name='phoxi',
      version='1.1.1.1',
      description='PhoXi driver',
      url='http://www.photoneo.com/',
      author='Matej Sladek',
      author_email='matejsladek10@gmail.com',
      packages=['phoxi'],
      package_data={'phoxi':["*.so*", "*.dll", "*.exp", "*.lib", "*.pyd"]},
      install_requires=['numpy'])