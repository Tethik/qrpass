#!/usr/bin/python

import unittest
import makeqr
import readqr
import random
import string

class TestCrt(unittest.TestCase):
	def test_keygen(self):
		master_pass = "".join(random.sample(string.letters, 10))
		aes_key = "".join(random.sample(string.letters, 16))
		# No IV dependency.
		key = makeqr.gen_aes_key(master_pass, aes_key)
		key2 = makeqr.gen_aes_key(master_pass, aes_key)		
		self.assertEqual(key,key2)
		
		# Wrong password should make different key.
		wrong_password_key = makeqr.gen_aes_key("test122", aes_key)
		self.assertNotEqual(key, wrong_password_key)
		
		# Wrong aes pub-key should make different key
		wrong_aes_key = makeqr.gen_aes_key(master_pass, "testtesttesttess")
		self.assertNotEqual(key, wrong_aes_key)
		
		# Different number of rounds should make different key
		orig_value = makeqr.NUMBER_OF_AES_ROUNDS
				
		while makeqr.NUMBER_OF_AES_ROUNDS == orig_value:
			makeqr.NUMBER_OF_AES_ROUNDS = random.randint(10, 1337)
		
		wrong_rounds_key = makeqr.gen_aes_key(master_pass, aes_key)
		self.assertNotEqual(key, wrong_rounds_key)
		
		# Reset and sanity check...
		makeqr.NUMBER_OF_AES_ROUNDS = orig_value
		key2 = makeqr.gen_aes_key(master_pass, aes_key)	
		self.assertEqual(key,key2)
		
	
	def test_encryption_decryption(self):
		master_pass = "".join(random.sample(string.letters, 10))
		aes_key = "".join(random.sample(string.letters, 16))
		plaintext = "".join(random.sample(string.letters, 50))
		
		key = makeqr.gen_aes_key(master_pass, aes_key)		
		iv, ciphertext = makeqr.encrypt(key, plaintext)
		self.assertNotEqual(plaintext, ciphertext)		
		self.assertEqual(plaintext, readqr.decrypt(key, iv, ciphertext))
		
	def test_qr_gen_and_load(self):
		master_pass = "".join(random.sample(string.letters, 10))
		aes_key = "".join(random.sample(string.letters, 16))
		plaintext = "".join(random.sample(string.letters, 50))		
		
		img = makeqr.encrypted_qr(master_pass, aes_key, plaintext)
		img.save("test.png")
		
		plain = readqr.decrypted_qr(master_pass, aes_key, "test.png")
		self.assertEqual(plaintext, plain)

if __name__ == '__main__':
    unittest.main()
