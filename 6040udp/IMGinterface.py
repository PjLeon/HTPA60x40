import numpy
import os
import cv2

'''
A module that deals with assembling matrices of captured 
temperature data, providing them to OpenCV and obtaining data of interest
'''

class Frame:
	''' Making a frame from arranged decoded packets '''
	
	def __init__(self, data)
		
