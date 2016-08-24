#!/usr/bin/env python

import pysodium as nacl

pk, sk = nacl.crypto_sign_keypair();
for i in pk: print format("%02h", i)
