
import socket
import os
import sys
import threading  # http://www.g-loaded.eu/2016/11/24/how-to-terminate-running-python-threads-using-signals/
import time
import datetime
import signal
import numpy
from itertools import chain
from pathlib import Path
import struct
import cv2
import pickle

import g


IP = '169.254.000.201'
PORT = 30444
BUFF_SIZE = 1300

call_msg = "Calling HTPA series devices"
bind_msg = "Bind HTPA series device"
release_msg = "X" #"x Release HTPA series device"
framereq_msg = "K" #K stream k frame

PACKET14_LEN = 1159
PACKET5_LEN = 1157
BYTE_FORMAT = "<h"  # Little-Endian b


cwd = os.getcwd()
output = os.path.join(cwd, 'output.txt') 

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(6)
sock.bind(('0.0.0.0', PORT))  # works with PORT = 0 ? Heimann UDP.pdf says to set receiving port to 30444 as well
print(sock)

def call():
    try:
        sock.sendto(call_msg.encode(), (IP,PORT))
        print(sock.recv(BUFF_SIZE))
        #print("Connected successfully to device under %s" % IP)
    except socket.timeout:
        sock.close()
        print("Can't connect to HTPA %s while initializing" % IP)
       
        
def bind():
    try:
        sock.sendto(bind_msg.encode(), (IP, PORT))
        print(sock.recv(BUFF_SIZE))
        #print("Bound to HTPA %s" % IP)
    except socket.timeout:
        sock.close()
        print("Failed to bind HTPA %s while initializing" % IP)


def release():
    sock.sendto(release_msg.encode(), (IP,PORT))
    print(sock.recv(BUFF_SIZE))
    print("Terminated HTPA {}".format(IP))

def receive():
    pixel_line = []
    while len(pixel_line) < 2400:
        packet = sock.recv(BUFF_SIZE)
        #print(len(packet))
        if len(packet) == PACKET14_LEN:
            container = struct.unpack('<B579h', packet)
            #with open(output, 'a') as file:
            #    file.write('{} \n'.format(container))
            pixel_line = list(chain(pixel_line, container[1:]))
            #n += 1
        elif len(packet) == PACKET5_LEN:
            container = struct.unpack('<B578h', packet)
            pixel_line = list(chain(pixel_line, container[1:85]))
            temp_array = numpy.array(pixel_line).reshape(40,60)
            #out = ''
            #out = out.join(map(str,pixel_line)
            #print(out)
            #out.join(pixel_line)
            with open('dump.pkl', 'ab') as file:
                pickle.dump(pixel_line, file)
            return temp_array
            #with open(output, 'a') as file:
            #    file.write('{} \n'.format(container))
            #n += 1
        else:
            print('weird packet of length: {} \n it says: {}'.format(len(packet), packet))
            #print(len(packet))
            #continue
        #print('n = {}'.format(n))

def stream():
    try:
        sock.sendto(framereq_msg.encode(), (IP, PORT))
        print("Streaming HTPA %s" % IP)
    except socket.timeout:
        sock.close()
        print("Failed to bind HTPA %s while initializing" % IP)
            #raise ServiceExit
      #  if not header:
       #     header2write = 'HTPA32x32d\n'
        #else:
        #    header2write = str(header).rstrip('\n')+('\n')
       # with open(self.fp, 'w') as file:
       #     file.write(header2write)




'''
class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass


def service_shutdown(signum, frame):
    print('Caught signal %d' % signum)
    raise ServiceExit
'''

