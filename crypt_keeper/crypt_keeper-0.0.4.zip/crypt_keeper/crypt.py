import os
import string
from random import SystemRandom
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

backend = default_backend()

def random(n):
    return os.urandom(n)

def random_salt():
    return random(16)

def random_iv():
    return random(16)

def random_key():
    return random(32)

def random_password(n=32, chars=None):
    if chars is None:
        chars = string.ascii_letters + string.digits + string.punctuation
    random = SystemRandom()
    return ''.join(random.choice(chars) for i in range(n))

def derive_key(password, salt):
    '''
    Derive 256 bit key from a password and salt combination.
    '''
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=backend
    )
    return kdf.derive(password.encode('utf8'))

def encrypt_aes_gcm(key, iv, plaintext):
    aes = algorithms.AES(key)
    gcm = modes.GCM(iv)
    cipher = Cipher(aes, gcm, backend=backend)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return encryptor.tag, ciphertext

def decrypt_aes_gcm(key, iv, tag, ciphertext):
    aes = algorithms.AES(key)
    gcm = modes.GCM(iv, tag)
    cipher = Cipher(aes, gcm, backend=backend)
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext

def encrypt_aes_cbc(key, iv, plaintext):
    aes = algorithms.AES(key)
    cbc = modes.CBC(iv)
    cipher = Cipher(aes, cbc, backend=backend)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return ciphertext

def decrypt_aes_cbc(key, iv, ciphertext):
    aes = algorithms.AES(key)
    cbc = modes.CBC(iv)
    cipher = Cipher(aes, cbc, backend=backend)
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext

def pad(data):
    padder = padding.PKCS7(128).padder()
    padded = padder.update(data) + padder.finalize()
    return padded

def unpad(data):
    unpadder = padding.PKCS7(128).unpadder()
    unpadded = unpadder.update(data) + unpadder.finalize()
    return unpadded
