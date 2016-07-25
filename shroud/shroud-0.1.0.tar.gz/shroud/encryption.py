from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


def generate_rsa_key_pair(modulus_bit_length=2048, passphrase=None):
    key = RSA.generate(modulus_bit_length)
    public_key = key.publickey().exportKey('PEM')
    private_key = key.exportKey('PEM', passphrase=passphrase)
    return public_key, private_key


def encrypt_secret_with_rsa_key(secret, public_key):
    public_key = RSA.importKey(public_key)
    cipher = PKCS1_OAEP.new(public_key)
    return cipher.encrypt(secret)


def decrypt_secret_with_rsa_key(ciphertext, private_key, passphrase=None):
    private_key = RSA.importKey(private_key, passphrase=passphrase)
    cipher = PKCS1_OAEP.new(private_key)
    return cipher.decrypt(ciphertext)
