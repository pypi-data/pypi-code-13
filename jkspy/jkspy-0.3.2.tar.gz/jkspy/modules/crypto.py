""" Dependency: Crypto """
from Crypto import Random
from Crypto.Hash import MD5, SHA, SHA256, SHA512, HMAC
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from jkspy.helpers import writeFile, readFile

def randbytes(length):
	return Random.new().read(length)

HASH_ALGORITHMS = { 'MD5':MD5,
					'SHA':SHA,
					'SHA256':SHA256,
					'SHA512':SHA512,
					'HMAC':HMAC }
def get_hash(message, method='sha256', hex=True):
	if method.upper() in HASH_ALGORITHMS.keys():
		if type(message) == str:
			message = message.encode('utf-8')
		if hex:
			return HASH_ALGORITHMS[method.upper()].new( message ).hexdigest()
		else:
			return HASH_ALGORITHMS[method.upper()].new( message ).digest()
	else:
		raise AttributeError('Hash algorithm ['+method.upper()+'] is not supported')

def get_checksum(filepath, method='md5', hex=True):
	if method.upper() in HASH_ALGORITHMS.keys():
		h = HASH_ALGORITHMS[method.upper()].new()
		chunk_size = 8192
		with open(filepath, 'rb') as f:
			while True:
				chunk = f.read(chunk_size)
				if len(chunk) == 0:
					break
				h.update(chunk)
		if hex:
			return h.hexdigest()
		else:
			return h.digest()
	else:
		raise AttributeError('Hash algorithm ['+method.upper()+'] is not supported')

HEXBIN_MAPPING = { '0' : '0000', '1' : '0001', '2' : '0010', '3' : '0011',
	 	   '4' : '0100', '5' : '0101', '6' : '0110', '7' : '0111',
		   '8' : '1000', '9' : '1001', 'a' : '1010', 'b' : '1011',
		   'c' : '1100', 'd' : '1101', 'e' : '1110', 'f' : '1111' }
BINHEX_MAPPING = { val : key for key, val in HEXBIN_MAPPING.items() }
def hex2bin(hexstr):
	binstr = ''
	for c in hexstr:
		binstr += HEXBIN_MAPPING[c]
	return binstr

def bin2hex(binstr):
	hexstr = ''
	for i in range(0, int(len(binstr) / 4)):
		subbin = binstr[i*4:i*4+4]
		hexstr += BINHEX_MAPPING[subbin]
	return hexstr

def b2hex(bytestr):
	return ''.join([hex(c)[2:].zfill(2) for c in bytestr])

def hex2b(hexstr):
	return bytes([ int(('0x'+hexstr[2*i:2*i+2]), 16) for i in range(0, int( len(hexstr)/2 ) ) ])

def make_key(key_size=16):
	return randbytes(key_size)

def add_padding(message, blocksize):
	return message + (blocksize - len(message) % blocksize) * chr(blocksize - len(message) % blocksize)

def remove_padding(message):
	return message[:-ord(message[len(message)-1:])]

def sencrypt(passphrase, plaintext, mode='CFB'):
	iv = randbytes(AES.block_size) #iv: 16 byte random salt (32 hex digits)
	key = get_hash(passphrase, 'sha256', hex=False) #key: 32 byte sha256 of passphrase
	cipher = AES.new( key, getattr(AES, 'MODE_'+mode), iv )
	paddedtext = add_padding( plaintext, len( iv ) )
	return iv + cipher.encrypt( paddedtext )

def sdecrypt(passphrase, ciphertext, mode='CFB'):
	iv = ciphertext[:AES.block_size] #iv: 16 byte random salt (32 hex digits)
	key = get_hash(passphrase, 'sha256', hex=False) #key: 32 byte sha256 of passphrase
	cipher = AES.new( key, getattr(AES, 'MODE_'+mode), iv )
	return remove_padding( cipher.decrypt(ciphertext[AES.block_size:]) ).decode()

KEYPAIR_ALGORITHMS = { 'RSA':RSA }
def make_keypair(method='RSA', bits=2048):
	if method.upper() in KEYPAIR_ALGORITHMS.keys():
		keypair = KEYPAIR_ALGORITHMS[method.upper()].generate(bits)
		# print("New keypair generated")
		# print(type(keypair))
		return keypair
	else:
		raise AttributeError('Keygen algorithm ['+method.upper()+'] is not supported')

def save_keypair(keypair, filepath, format='PEM'):
	pw = input("Password for the keypair (leave blank if encrypting the keys is unnecessary) >> ")
	if pw:
		prvkey = keypair.exportKey(format, pw)
	else:
		prvkey = keypair.exportKey()
	writeFile(filepath+'.private', prvkey, True)

	pubkey = keypair.publickey().exportKey()
	writeFile(filepath+'.public', pubkey, True)
	
	print("--------------------------")
	print(" Generating RSA keypair")
	print("--------------------------")
	print(prvkey)
	print('    > Private key saved as '+filepath+'.private')
	print('--------------------------')
	print(pubkey)
	print('    > Public key saved as '+filepath+'.public')
	print('--------------------------')

def open_keypair(keypath):
	keystr = readFile(keypath, True)
	try:
		keys = RSA.importKey(keystr)
	except ValueError:
		print("Enter password for the private key")
		pw = input(' >> ')
		try:
			keys = RSA.importKey(keystr, pw)
		except ValueError:
			print("...Wrong password")
			raise ValueError("Wrong Password")
	return keys

def encrypt(pubkey, plaintext):
	return pubkey.encrypt(plaintext.encode('utf-8'), 32)[0]

def decrypt(keypair, ciphertext):
	return keypair.decrypt(ciphertext)

def sign(keypair, message, isFile=False):
	if isFile:
		mhash = get_checksum(message, 'sha256', False)
	else:
		mhash = get_hash(message, 'sha256', False)
# 	print(mhash)
	return keypair.sign(mhash, '')

def verify(publickey, message, signature, isFile=False):
	if isFile:
		return publickey.verify( get_checksum(message, 'sha256', False), signature )
	else:
		return publickey.verify( get_hash(message, 'sha256', False), signature )

# def verify(keypair, message):
# 	mhash = get_hash(message, 'sha256', False)
# 	keypair.publickey.verify(  , )

def test_rsa():
	print("\n\n>>> Testing RSA")
	keypair = make_keypair()
	ciphertext = encrypt(keypair.publickey(), 'Hello World')
	print("CipherByte: "+ciphertext.__str__())

	plaintext = decrypt(keypair, ciphertext)
	print("PlainByte: "+plaintext.decode())

	signature = sign(keypair, plaintext)
	print("Signature: "+signature.__str__())

	print("Verification successful") if keypair.publickey().verify( get_hash('Hello World', hex=False), signature ) else print("Verification failure")

	print(">>> END RSA Test")

def main():
	ciphertext = sencrypt('password', 'Hello World')
	print("CipherHex: "+b2hex(ciphertext).__str__())
	print("CipherByte: "+hex2b(b2hex(ciphertext)).__str__())
	plaintext = sdecrypt('password', ciphertext)
	print("PlainHex: "+b2hex(plaintext).__str__())
	print("PlainByte: "+plaintext.__str__()	)

	test_rsa()

	print(">>> Routine End")

# main()
