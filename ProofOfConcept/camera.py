#!/usr/bin/python

import pygame
import pygame.camera
from pygame.locals import *
import pygame.image
import readqr
import zbar
from PIL import Image
import base64
import pyperclip
import os

os.environ['PYGAME_CAMERA'] = 'opencv'

pygame.init()
pygame.camera.init()

try:
	aes_key = open("qrpass.pub").read()
except:
	print "Could not find a AES keyfile."
	print "Please create a AES keyfile first. This is used together with your master password to generate the master key used for encryption."
	exit(1)



class Capture(object):
    def __init__(self):
        self.size = (640,480)
        # create a display surface. standard pygame stuff
        self.display = pygame.display.set_mode(self.size, 0)
        self.scanner = zbar.ImageScanner()
        
        # this is the same as what we saw before
        self.clist = pygame.camera.list_cameras()
        if not self.clist:
            raise ValueError("Sorry, no cameras detected.")
        self.cam = pygame.camera.Camera(self.clist[0], self.size)
        self.cam.start()
		
        # create a surface to capture to.  for performance purposes
        # bit depth is the same as that of the display surface.
        self.snapshot = pygame.surface.Surface(self.size, 0, self.display)

    def get_and_flip(self):
        # if you don't want to tie the framerate to the camera, you can check 
        # if the camera has an image ready.  note that while this works
        # on most cameras, some will never return true.
        if self.cam.query_image():
            self.snapshot = self.cam.get_image(self.snapshot)

        # blit it to the display surface.  simple!
        self.display.blit(self.snapshot, (0,0))
        pygame.display.flip()
        
        print self.cam.get_size()
        
        if self.find_qr_code():			
			master_password = raw_input("Master password: ")
			pygame.image.save(self.snapshot, "img.png")
			password = readqr.decrypted_qr(master_password, aes_key, "img.png")
			pyperclip.copy(password)
			print "Password copied to clipboard!"			
			self.cam.stop()
			exit(0)
        
    def find_qr_code(self):
		# convert to PIL
		data = pygame.image.tostring(self.snapshot, 'RGBA')
		pil = Image.fromstring('RGBA', self.size, data).convert('L')
		# then convert to zbar image.
		width, height = self.size
		raw = pil.tostring()
		# wrap image data
		image = zbar.Image(width, height, 'Y800', raw)

		# scan the image for barcodes
		self.scanner.scan(image)
		
		# extract results
		for symbol in image:
			print symbol
		# do something useful with results
			if str(symbol.type) != 'QRCODE':
				continue		
			b64 = symbol.data
			#~ print b64
			data = base64.b64decode(b64)
			iv = data[:16]		
			ciphertext = data[16:]		
			return True

    def main(self):
        going = True
        while going:
            events = pygame.event.get()
            for e in events:
                if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                    # close the camera safely
                    self.cam.stop()
                    going = False

            self.get_and_flip()

#~ camlist = pygame.camera.list_cameras()
#~ cam = pygame.camera.Camera(camlist[0],(1920,1080))
#~ cam.start()
#~ img = cam.get_image()
#~ pygame.image.save(img, "img.png")

c = Capture()
c.main()
