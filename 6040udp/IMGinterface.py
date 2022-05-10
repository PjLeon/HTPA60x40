import numpy
import os
import cv2
import time

import g

'''
A module that deals with assembling matrices of captured 
temperature data, providing them to OpenCV and obtaining data of interest
'''

'''
def frame_builder(pixel_line):
    line = numpy.array(pixels)
    frame = line.reshape(40,60)
    #frame_scaled = frame * 255.0/frame.max()
    #frame = (frame - 2731)/10 #convert to Celcius
    frame_scaled = (255*(frame - numpy.min(frame))/numpy.ptp(frame)).astype('uint8')
    return frame_scaled
'''
def output_stream(frame):
    #print(frame)
    frame_scaled = (255*(frame - numpy.min(frame))/numpy.ptp(frame)).astype('uint8')
    #ret, thresh = cv2.threshold(frame_scaled,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    frame_flip = cv2.flip(frame_scaled, 0)
    cv2.imshow('iseethis', cv2.resize(frame_flip,(360,240)))
    cv2.waitKey(10)
    #return frame_scaled
    
def processing(frame):
    #cv2.bilateral
    #cv2.median
    pass

def run_loop(gpline):
    #global terminate_flag
    
    time.sleep(0.5)
    #n += 1
    gpline[0] += 1
    g.pixel_line = gpline
    #return output
