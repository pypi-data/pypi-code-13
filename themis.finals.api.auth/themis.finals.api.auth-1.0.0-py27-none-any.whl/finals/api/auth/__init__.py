# -*- coding: utf-8 -*-
from __future__ import absolute_import
from os import getenv, urandom
from base64 import urlsafe_b64decode, urlsafe_b64encode
from hashlib import sha256


def get_nonce_size():
    return int(getenv('THEMIS_FINALS_NONCE_SIZE', '16'))


def issue_token(name):
    nonce = urandom(get_nonce_size())
    secret = urlsafe_b64decode(getenv('THEMIS_FINALS_{0}_KEY'.format(name)))

    h = sha256()
    h.update(nonce)
    h.update(secret)

    nonce_bytes = nonce
    digest_bytes = h.digest()

    token_bytes = nonce_bytes + digest_bytes
    return urlsafe_b64encode(token_bytes)


def issue_checker_token():
    return issue_token('CHECKER')


def verify_token(name, token):
    if token is None:
        return False

    nonce_size = get_nonce_size()

    token_bytes = urlsafe_b64decode(token.encode('utf-8'))

    if len(token_bytes) != 32 + nonce_size:
        return False

    nonce = token_bytes[0:nonce_size]
    received_digest_bytes = token_bytes[nonce_size:]

    secret = urlsafe_b64decode(getenv('THEMIS_FINALS_{0}_KEY'.format(name)))

    h = sha256()
    h.update(nonce)
    h.update(secret)

    digest_bytes = h.digest()

    return digest_bytes == received_digest_bytes


def verify_master_token(token):
    return verify_token('MASTER', token)
