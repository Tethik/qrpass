#!/usr/bin/python

from Crypto.Hash import SHA256
from Crypto import Random
from Crypto.Cipher import AES

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
		
		
if __name__ == "__main__":
	key = gen_aes_key("test", "testtesttesttest")
	key2 = gen_aes_key("test", "testtesttesttest")
	assert(key == key2)
	
	


