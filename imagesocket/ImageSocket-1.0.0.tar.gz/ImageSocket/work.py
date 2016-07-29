import socket
import base64
import numpy as np
import rtp
import cv2
import logg
from bluetooth import *

"""
	------	Python Plugin ( ImageSocket)	------
	This plugin is written by SunnerLi in 2016 - 04
	This class define the sub-socket to perform receiving image
	The project is follow MIT License
"""

class ImageSocket_Work():
    """
        This class define the working socket contain and method
    """
    workSock = None				# The working socket object
    workType = None				# The working type( TCP or BT ?)
    hadSetTimeout = False		# The flag to record if set the timeout of the socket
    
    TCP = 0						# Constant of type
    BT = 2						# Constant of type

    def __init__(self, _type):
    	"""
    		Constructor of working socket
    	"""
    	self.workType = _type

    def setWorkSocket(self, sock):
    	"""
    		Set the socket object.
    		Or the afterware process would give error
    	"""
    	self.workSock = sock

    def close(self):
    	"""
    		Close the tcp socket
    	"""
    	if not type(self.workSock) == type(None):
    		self.workSock.close()

    def recv(self, size):
    	"""
    		Recv the image string from the opposite
    		This function force to set the timeout
    	"""
    	self.workSock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 200000)  # Buffer size 8192
    	if not self.hadSetTimeout:
    		self.workSock.settimeout(10)    
    	roughPng = ""
    	while True:
    		try:
    			data = self.workSock.recv(2000000)
    			logg.LOGI("length: ", len(data))
    			roughPng += data
    			if len(data) < 66:
    				break
    			self.workSock.settimeout(0.5)
    		except socket.timeout:
    			data = ""
    			break   
    	# Transform image string to numpy (Through OpenCV)
    	png = self.cleanHeader(roughPng)
    	png = base64.b64decode(png)
    	png = self.formImgArr(png)
    	png = self.oneD2Numpy(png)
    	return png

    def cleanHeader(self, png):
    	"""
    		Drop the header (No consider RTP information in TCP)
    	"""
        headerLength = 0;
        if self.workType == self.TCP:
    	    headerLength = 65;
        elif self.workType == self.BT:
            headerLength = 45;
        png = png[:len(png)-headerLength]
    	copy = png
    	png = ""    
		
    	# Get the 1st header to show speed
    	header = copy[:headerLength]
    	#r = rtp.RTP()
    	#r.decode(header)   
    	# Drop the rest
		
        if self.workType == self.TCP:
    	    while len(copy) > 0:
    	    	piece = copy[headerLength:1445]
    	    	png += piece
    	    	copy = copy[1445:]
        elif self.workType == self.BT:
            while len(copy) > 0:
    	    	piece = copy[headerLength:60045]
                print "picture piece length: ", len(piece)
    	    	png += piece
    	    	copy = copy[60045:]
    	return png

    def formImgArr(self, data):
    	"""
    		Change the image string into 1D array
    	"""
    	png = []
    	for i in range(len(data)):
    		png.append(ord(data[i]))
    	return png

    def oneD2Numpy(self, data):
    	"""
    		Decode the 1D image by the OpenCV
    	"""
    	data = np.asarray(data, dtype=np.uint8)
    	data = cv2.imdecode(data, 1)
    	return data