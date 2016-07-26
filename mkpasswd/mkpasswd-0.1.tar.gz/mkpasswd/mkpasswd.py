#!/usr/bin/python
import crypt
import sys
import getpass

Hashers = {
        'SHA512': lambda x: print(crypt.crypt(x, crypt.mksalt(crypt.METHOD_SHA512))),
        'SHA256': lambda x: print(crypt.crypt(x, crypt.mksalt(crypt.METHOD_SHA256))),
        'MD5':    lambda x: print(crypt.crypt(x, crypt.mksalt(crypt.METHOD_MD5)))
    }

algorithm = input("Algorithm(SHA512, SHA256 or MD5): ").upper()
password = getpass.getpass("Password: ")
verified = getpass.getpass("Verify Password: ")

if not algorithm in Hashers:
	print("Invalid Hashing algorithm, please use SHA512, SHA256 or MD5")
	sys.exit()

if password == verified: 
	Hashers[algorithm](password)
else:
	print("mismatched passwords.")
   