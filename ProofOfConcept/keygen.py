#!/usr/bin/python

from Crypto import Random
from optparse import OptionParser
import qrcode

options = OptionParser(usage='%prog file=qrpass.pub', description='Generate a random 256-bit AES key')

if __name__ == "__main__":
	opts, args = options.parse_args()
	filename = "qrpass.pub"
	if len(args) > 1:
		filename = args[0]
	rng = Random.new()
	key = rng.read(32)
	with file(filename, "wb") as f:
		f.write(key)
	qr = qrcode.make(key)
	qr.save(filename + ".png")
	qr.show()

