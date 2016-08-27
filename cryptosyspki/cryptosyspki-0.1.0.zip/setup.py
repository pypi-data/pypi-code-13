from distutils.core import setup
setup(name='cryptosyspki',
      version='0.1.0',
      description='Python interface to CryptoSys PKI',
      author='David Ireland',
      url='http://www.cryptosys.net/pki/',
      platforms=['Windows'],
      py_modules=['cryptosyspki'],
      data_files=[('.', ['README.md']), ('test', ['test/pkiPythonTestFiles.zip'])],
      )
