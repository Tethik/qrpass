#!/usr/bin/python

from Crypto.Hash import SHA256
from Crypto import Random
from Crypto.Cipher import AES
import qrcode
from optparse import OptionParser
import base64

options = OptionParser(usage='%prog', description='Create a qr code image using a master password.')

NUMBER_OF_AES_ROUNDS = 10000

# Using same key generation algorithm as Keepass
# SHA256 -> 6000 times AES (ECB) encryption -> SHA256.
# Padding to make dictionary attacks harder.
# See: http://keepass.info/help/base/security.html#secdictprotect
# https://github.com/bpellin/keepassdroid/blob/master/src/com/keepassdroid/crypto/finalkey/AndroidFinalKey.java
def gen_aes_key(master_password, aes_key):	
	key = SHA256.new(master_password).digest()
	aes = AES.new(aes_key, AES.MODE_ECB)
	for _ in xrange(NUMBER_OF_AES_ROUNDS):
		key = aes.encrypt(key)
	key = SHA256.new(key).digest()
	return key

# Encrypt using aes in CFB mode. Return ciphertext and iv.
def encrypt(master_aes_key, plaintext):
	rng = Random.new()
	iv = rng.read(16)
	aes = AES.new(master_aes_key, AES.MODE_CFB, iv)
	ciphertext = aes.encrypt(plaintext)
	return (iv, ciphertext)
	
def encrypted_qr(master_pass, aes_key, content):
	key = gen_aes_key(master_pass, aes_key)
	iv, ciphertext = encrypt(key, content)	
	b64 = base64.b64encode(iv + ciphertext)
	return qrcode.make(base64.b64encode(iv + ciphertext))
	
if __name__ == "__main__":
	opts, args = options.parse_args()
	#~ if len(args) < 2:
		#~ options.print_help()
		#~ exit(1)
	
	try:
		aes_key = open("qrpass.pub").read()
	except:
		print "Please create a AES keyfile first. This is used together with your master password to generate the master key used for encryption."
		exit(1)
	
	filename = raw_input("Save to filename: ")
	master_password = raw_input("Master password: ")
	new_password = raw_input("Password to encrypt: ")	
			
	
	img = encrypted_qr(master_password, aes_key, new_password)
	img.show()
	img.save(filename)
	
	


