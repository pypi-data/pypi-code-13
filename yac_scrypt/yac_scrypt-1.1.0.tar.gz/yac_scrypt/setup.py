from distutils.core import setup, Extension

yac_scrypt_module = Extension('yac_scrypt',
								sources = ['scryptmodule.c',
                                          './scrypt-jane/scrypt-jane.c'],
							include_dirs=['.', './scrypt-jane', './scrypt-jane/code'])

setup (name = 'yac_scrypt',
       version = '1.1',
       description = 'Bindings for scrypt-jane proof of work used by LEOcoin',
       ext_modules = [yac_scrypt_module])
