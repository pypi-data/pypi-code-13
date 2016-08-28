from distutils.core import setup
setup(name='firmasatpy',
      version='0.1.1',
      description='Python interface to CryptoSys FirmaSAT',
      author='David Ireland',
      url='http://www.cryptosys.net/firmasat/',
      platforms=['Windows'],
      py_modules=['firmasat'],
      data_files=[('.', ['README.rst', 'firmasatdoc.chm']), ('test', ['test/firmasatPyTestFiles.zip'])],
      )
