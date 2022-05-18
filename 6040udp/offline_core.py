"""
Python program that connects to Heimann HTPA sensors given their IP addresses (in settings file) and records data captured to TXT files. 
Supports recording mutliple sensors at the same time. This tool is supposed to help developing multi-view thermopile sensor array monitoring system.
"""
import socket
import os
import sys
#import threading  # http://www.g-loaded.eu/2016/11/24/how-to-terminate-running-python-threads-using-signals/
import time
#import datetime
import signal
from pathlib import Path
import struct
import pickle
import numpy

import g
import HTPAinterface
import IMGinterface2

cwd = os.getcwd()
print(cwd)
dump = os.path.join(cwd, 'dump3.pkl') 

f = open(dump, 'rb')

median = 0
def unpickler():
    try: 
        pixel_line = pickle.load(f)
        temp_array = numpy.array(pixel_line).reshape(40,60)
    except EOFError:
        sys.exit()
    return temp_array


def terminate(signum, frame):
    #global terminate_flag
    g.terminate_flag = True
    HTPAinterface.release()
    print('caught {}'.format(signum))
    #raise SystemExit('I just sudokud myself')


def fps(ticker, start_t):
    fps = ticker / (time.time() - start_t)
    print('FPS = {}'.format(fps))


def main():
    print('Starting main')
    global median
    g.init()
    signal.signal(signal.SIGTERM, terminate)
    signal.signal(signal.SIGINT, terminate)
    print('Entering main hyperloop')
    print('pid: {}'.format(os.getpid()))
    start_t = time.time()
    fps_interval = 10 #seconds between avg fps calculations
    ticker = 0
    while not g.terminate_flag:
        ticker += 1
        temp_array = unpickler()
        f_clip = IMGinterface2.clip(temp_array)
        IMGinterface2.edge(f_clip, True)
        IMGinterface2.gradient(f_clip, True)
        IMGinterface2.threshold(f_clip, temp_array, True)
        if (time.time() - start_t ) > fps_interval:
            fps(ticker, start_t)
            ticker = 0
            start_t = time.time()
            


if __name__ == "__main__":
    main()
