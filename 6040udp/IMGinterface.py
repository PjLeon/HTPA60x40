import numpy
import os
import cv2
import time

import g

'''
A module that deals matrices of captured 
temperature data, providing them to OpenCV and obtaining areas of interest
and calculates the decrease per pixel be.

Temp range for converting to grayscale output values: 
50 - 100 deg (0 to 255) , corresponds to 
sensor readings 3230 - 3731 (K*10) 
'''
CLIP_LOW = 3230
CLIP_HIGH = 3730
CLIP_DELTA = CLIP_HIGH - CLIP_LOW

ker = numpy.array([[0, -1, 0],[-1, 5, -1],[0, -1, 0]])

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
    frame = cv2.flip(frame, 0)
    f_half = frame
    f_half[20:40,0:60] = 0
    f_half[6:10,24:35] = 0
    f_clip = numpy.clip(f_half, CLIP_LOW, CLIP_HIGH)
    f_gray = (255*(f_clip - CLIP_LOW)/CLIP_DELTA).astype('uint8')
    float_gray = (255*(f_clip - CLIP_LOW)/CLIP_DELTA).astype('float32')
    #f_gray = cv2.fastNlMeansDenoising(f_gray, h=71, templateWindowSize=3, searchWindowSize=3)
    #float_gray = cv2.GaussianBlur(f_gray, (3,3), 0)
    #f_gray = cv2.medianBlur(f_gray, 3)
    #f_gray = cv2.bilateralFilter(float_gray, 7, 20, 20) #img, diameter, sigma color, sigma space
    f_sharp = cv2.filter2D(float_gray, -1, ker)
    ret, molten_f = cv2.threshold(f_gray,250,255,cv2.THRESH_BINARY)
    #molten_f = cv2.adaptiveThreshold(f_gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, 3, 2)
    ret, solid_f = cv2.threshold(f_gray,1,255,cv2.THRESH_OTSU) 
    #solid_f = cv2.adaptiveThreshold(f_gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, 19, 10) # region size, C threshold adjust value
    delta_f = solid_f - molten_f
    #delta_f = cv2.erode(delta_f, None, 1)
    molten_x, molten_y = numpy.nonzero(molten_f)
    #solid_x, solid_y = numpy.nonzero(delta_f)
    molten_arr = numpy.transpose(numpy.array([frame[molten_x, molten_y], molten_x, molten_y]))
    #extract values in the same frame column, i.e. having same x value:
    columns = numpy.unique(molten_arr[:,1])
    #for i in columns:
     #   melt_temp_line = molten[molten[:,1]==i]
    #sobelx = cv2.Sobel(src=f_gray, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5) # Sobel Edge Detection on the X axis
    #sobely = cv2.Sobel(src=f_gray, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5) # Sobel Edge Detection on the Y axis
    #sobelxy = cv2.Sobel(src=f_gray, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5) # Combined X and Y Sobel Edge Detection
    
    edge_lap = cv2.Laplacian(f_gray,cv2.CV_32F,ksize = 1)
    f_gray_8b = cv2.convertScaleAbs(f_sharp)
    edges_c = cv2.Canny(f_gray,10, 250, apertureSize=3, L2gradient = True)
    
    
    #contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    #cv2.drawContours(frame_gray, contours, -1, (255, 230, 255), 1, cv2.LINE_AA)
    cv2.imshow('gray_clipped', cv2.resize(f_gray,(360,240), fx=0, fy=0, interpolation = cv2.INTER_NEAREST))
    cv2.imshow('molten_px', cv2.resize(molten_f,(360,240), fx=0, fy=0, interpolation = cv2.INTER_NEAREST))
    cv2.imshow('solid_px', cv2.resize(delta_f,(360,240), fx=0, fy=0, interpolation = cv2.INTER_NEAREST))
    
    cv2.imshow('laplacian', cv2.resize(edge_lap,(360,240), fx=0, fy=0, interpolation = cv2.INTER_NEAREST))
    #cv2.imshow('sobel', cv2.resize(sobelxy,(360,240)))
    cv2.imshow('canny', cv2.resize(edges_c, (360, 240), fx=0, fy=0, interpolation = cv2.INTER_NEAREST))
    cv2.waitKey(50)
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
