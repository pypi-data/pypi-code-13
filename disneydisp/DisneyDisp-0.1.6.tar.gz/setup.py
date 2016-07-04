from setuptools import setup

setup(name='DisneyDisp',
      version='0.1.6',
      description='A python implementation of the \"Scene Reconstruction from High Spatio-Angular Resolution Light Fields\". For more information see https://www.disneyresearch.com/project/lightfields/.',
      url='https://github.com/manuSrep/DisneyDispPy.git',
      author='Marcel Gutsche, Manuel Tuschen',
      author_email='Manuel_Tuschen@web.de',
      license='GPL3 License',
      packages=['DisneyDisp'],
      install_requires=["scipy","numpy","scikit-image","matplotlib","numba","h5py","progressbar2","easyScripting"],
      zip_safe=False,
      scripts=['bin/disney', 'bin/clif2lf', 'bin/dmap2hdf5', 'bin/imgs2lf', 'bin/lf2epi.py']
      )
