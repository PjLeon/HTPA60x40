
import socket
import os
import sys
import threading  # http://www.g-loaded.eu/2016/11/24/how-to-terminate-running-python-threads-using-signals/
import time
import datetime
import signal
from pathlib import Path
import struct
# import cv2

IP_LIST_FP = os.path.join("recording", "settings", "devices.txt")
IP = '169.254.000.201'
PORT = 30444
BUFF_SIZE = 1300

call_msg = "Calling HTPA series devices"
bind_msg = "Bind HTPA series device"
release_msg = "x Release HTPA series device"
framereq_msg = "k" #K stream k frame

PACKET14_LEN = 1159
PACKET5_LEN = 1157
BYTE_FORMAT = "<h"  # Little-Endian b

    


def decode_packets(packet1, packet2):
    


def call_HTPA():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)
    sock.bind(('0.0.0.0', PORT))  # works with PORT = 0 ? Heimann UDP.pdf says to set receiving port to 30444 as well
    print(sock)
    try:
        sock.sendto(call_msg.encode(), (IP,PORT))
        print(sock.recv(BUFF_SIZE))
        #print("Connected successfully to device under %s" % IP)
    except socket.timeout:
        sock.close()
        print("Can't connect to HTPA %s while initializing" % IP)
       
        
def bind_HTPA():
    try:
        sock.sendto(bind_msg.encode(), (IP, PORT))
        print(sock.recv(BUFF_SIZE))
        #print("Bound to HTPA %s" % IP)
    except socket.timeout:
        self.sock.close()
        print("Failed to bind HTPA %s while initializing" % self.device.ip)


def stream_HTPA

def release_HTPA


class Recorder(threading.Thread):
    def __init__(self, device, fp, T0, header=None):
        threading.Thread.__init__(self)
        self.shutdown_flag = threading.Event()
        self.device = device
        self.fp = fp
        self.T0 = T0
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(1)
        self.sock.bind((socket.gethostbyname(socket.gethostname()), 0))

        try:
            self.sock.sendto(HTPA_CALLING_MSG.encode(), self.device.address)
            _ = self.sock.recv(BUFF_SIZE)
            print("Connected successfully to device under %s" % self.device.ip)
        except socket.timeout:
            self.sock.close()
            print("Can't connect to HTPA %s while initializing" % self.device.ip)
            raise ServiceExit
        try:
            self.sock.sendto(HTPA_BIND_MSG.encode(), self.device.address)
            self.sock.recv(BUFF_SIZE)
            self.sock.sendto(HTPA_STREAM_MSG.encode(), device.address)
            print("Streaming HTPA %s" % self.device.ip)
        except socket.timeout:
            self.sock.close()
            print("Failed to bind HTPA %s while initializing" % self.device.ip)
            raise ServiceExit
      #  if not header:
       #     header2write = 'HTPA32x32d\n'
        #else:
        #    header2write = str(header).rstrip('\n')+('\n')
       # with open(self.fp, 'w') as file:
       #     file.write(header2write)

    def run(self):
        print('Thread [TPA] #%s started' % self.ident)

        packet1, packet2 = None, None
        while not self.shutdown_flag.is_set():
            try:
                packet_a = self.sock.recv(BUFF_SIZE)
                packet_b = self.sock.recv(BUFF_SIZE)
            except socket.timeout:
                self.sock.sendto(HTPA_RELEASE_MSG.encode(),
                                 self.device.address)
                print("Terminated HTPA {}".format(self.device.ip))
                self.sock.close()
                print("Timeout when expecting stream from HTPA %s" %
                      self.device.ip)
                raise ServiceExit
            timestamp = time.time() - self.T0
            if not (packet_a and packet_b):
                continue
            packet_str = decode_packets(*order_packets(packet_a, packet_b))
            with open(self.fp, 'a') as file:
                file.write("{}t: {:.2f}\n".format(packet_str, timestamp))

        # CLEANUP !!!
        self.sock.sendto(HTPA_RELEASE_MSG.encode(), self.device.address)
        print("Terminated HTPA {}".format(self.device.ip))

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

