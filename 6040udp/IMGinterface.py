import numpy
import os
import cv2

'''
A module that deals with assembling matrices of captured 
temperature data, providing them to OpenCV and obtaining data of interest
'''

def frame_builder(pixels):
    line = numpy.array(pixels)
    frame = line.reshape(40,60)
    print(frame)
