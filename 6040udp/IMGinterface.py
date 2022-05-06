import numpy
import os
import cv2
import time

import g

'''
A module that deals with assembling matrices of captured 
temperature data, providing them to OpenCV and obtaining data of interest
'''

def frame_builder(pixels):
    line = numpy.array(pixels)
    frame = line.reshape(40,60)
    print(frame)
    
def run_loop(gpline):
    #global terminate_flag
    
    time.sleep(0.5)
    #n += 1
    gpline[0] += 1
    g.pixel_line = gpline
    #return output
