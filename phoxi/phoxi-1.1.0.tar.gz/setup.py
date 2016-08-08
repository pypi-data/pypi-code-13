from distutils.core import setup

setup(name='phoxi',
      version='1.1.0',
      description='PhoXi driver',
      url='http://www.photoneo.com/',
      author='Matej Sladek',
      author_email='matejsladek10@gmail.com',
      packages=['phoxi'],
      package_data={'phoxi':["*.so", "*.lib", "*.pyd"]},
      install_requires=['numpy'])
