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

ker = numpy.array([[0, -1, 0],[-1, 5, -1],[0, -1, 0]]) #sharpening kernel
f_median = 0
ker_e = numpy.ones((3,3), 'uint8')
#ker_e = numpy.array([[0, 0, 0],[1, 1, 1],[1, 0, 1]]).astype('uint8')
#ker_e = numpy.array([[1, 1],[1, 1]]).astype('uint8')

def clip(frame):
    frame = cv2.flip(frame, 0)
    f_half = frame
    f_half[20:40,0:60] = 0
    #f_half[6:10,24:35] = 0
    f_clip = numpy.clip(f_half, CLIP_LOW, CLIP_HIGH)

    return f_clip


def edge(f_clip, show = False):
    f_gray = gray_i8(f_clip)
    f_gray = blur(f_gray)

    sigma = 0.33
    f_median = numpy.median(f_gray)
    low = int(max(0,(1.0 - sigma)*f_median))
    high = int(min(255, (1.0 + sigma)*f_median))
    edges_c = cv2.Canny(f_gray, low, high, apertureSize=3, L2gradient = True)
    
    #edges_d = cv2.erode(edges_c, None, ker_e)
    edges_d = cv2.dilate(edges_c, None, 1)
    #edges_d = cv2.morphologyEx(edges_c, cv2.MORPH_CLOSE, ker_e)
    
    contours, hierarchy = cv2.findContours(edges_c, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    for n in contours:
        #print(cv2.contourArea(n))
        #print(n)
        #print(cv2.contourArea(n))
        if cv2.contourArea(n) > 20:
            cv2.drawContours(f_gray, [n], -1, (225, 225, 225), 1, cv2.LINE_AA)
    #cv2.drawContours(f_gray, contours, -1, (225, 225, 225), 1, cv2.LINE_AA)
    if show:
        cv2.imshow('canny', cv2.resize(edges_c, (360, 240), fx=0, fy=0, interpolation = cv2.INTER_NEAREST))
        cv2.imshow('gray', cv2.resize(f_gray, (360, 240), fx=0, fy=0, interpolation = cv2.INTER_NEAREST))
        cv2.imshow('eroded', cv2.resize(edges_d, (360, 240), fx=0, fy=0, interpolation = cv2.INTER_NEAREST))
        cv2.waitKey(5)


def gradient(f_clip, show = False):
    f_gray = gray_f32(f_clip)
    f_gray = blur(f_gray)
    edge_lap = cv2.Laplacian(f_gray,cv2.CV_32F,ksize = 1)
    #f_gray_8b = cv2.convertScaleAbs(f_sharp)
    
    #sobelx = cv2.Sobel(src=f_gray, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5) # Sobel Edge Detection on the X axis
    #sobely = cv2.Sobel(src=f_gray, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5) # Sobel Edge Detection on the Y axis
    sobelxy = cv2.Sobel(src=f_gray, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=1) # Combined X and Y Sobel Edge Detection

    if show:
        cv2.imshow('laplacian', cv2.resize(edge_lap, (360, 240), fx=0, fy=0, interpolation = cv2.INTER_NEAREST))
        cv2.imshow('sobel', cv2.resize(sobelxy, (360, 240), fx=0, fy=0, interpolation = cv2.INTER_NEAREST))
        cv2.waitKey(5)
    
def threshold(f_clip, show = False):
    f_gray = gray_i8(f_clip)
    
    ret, molten_f = cv2.threshold(f_gray,250,255,cv2.THRESH_BINARY)
    #molten_f = cv2.adaptiveThreshold(f_gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, 3, 2)
    ret, solid_f = cv2.threshold(f_gray,2,255,cv2.THRESH_OTSU) 
    #solid_f = cv2.adaptiveThreshold(f_gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, 19, 10) # region size, C threshold adjust value
    delta_f = solid_f - molten_f
    #delta_f = cv2.erode(delta_f, None, 2)
    molten_x, molten_y = numpy.nonzero(molten_f)
    #solid_x, solid_y = numpy.nonzero(delta_f)
    molten_arr = numpy.transpose(numpy.array([f_clip[molten_x, molten_y], molten_x, molten_y]))
    #extract values in the same frame column, i.e. having same x value:
    columns = numpy.unique(molten_arr[:,1])
    #for i in columns:
     #   melt_temp_line = molten[molten[:,1]==i]
    if show:
        cv2.imshow('molten_px', cv2.resize(molten_f,(360,240), fx=0, fy=0, interpolation = cv2.INTER_NEAREST))
        cv2.imshow('solid_px', cv2.resize(delta_f,(360,240), fx=0, fy=0, interpolation = cv2.INTER_NEAREST))
        cv2.waitKey(5)

    
def gray_f32(f_clip):
    float_gray = (255*(f_clip - CLIP_LOW)/CLIP_DELTA).astype('float32')
    return float_gray
    
def gray_i8(f_clip):
    int_gray = (255*(f_clip - CLIP_LOW)/CLIP_DELTA).astype('uint8')
    return int_gray

def blur(f_gray):
    #f_gray = cv2.fastNlMeansDenoising(f_gray, h=71, templateWindowSize=3, searchWindowSize=3)
    filtered = cv2.GaussianBlur(f_gray, (3,3), 10)
    #filtered = cv2.medianBlur(f_gray, 5)
    #filtered = cv2.bilateralFilter(f_gray, 5, 20, 20) #img, diameter, sigma color, sigma space
    return filtered

def sharp(float_gray, show = False):
    f_sharp = cv2.filter2D(float_gray, -1, ker)
    

