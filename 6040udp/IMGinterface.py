import numpy
import os
import cv2
import time

import g

'''
A module that deals with assembling matrices of captured 
temperature data, providing them to OpenCV and obtaining data of interest.

Temp range for converting to grayscale 40 - 250 deg (0 to 255) , corresponds to 
sensor readings 3100 - 5230 (K*10) 
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
    frame_gray = (255*(frame - numpy.min(frame))/numpy.ptp(frame)).astype('uint8')
    frame_gray = cv2.flip(frame_gray, 0)
    ret, thresh = cv2.threshold(frame_gray,70,255,cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(frame_gray, contours, -1, (255, 230, 255), 1, cv2.LINE_AA)
    cv2.imshow('iseethis', cv2.resize(frame_gray,(360,240)))
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
