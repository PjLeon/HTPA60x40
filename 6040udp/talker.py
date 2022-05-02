import socket
import os


call_msg = "Calling HTPA series devices"
bind_msg = "Bind HTPA series device"
release_msg = "x Release HTPA series device"
framereq_msg = "X"

cwd = os.getcwd()
output = os.path.join(cwd, 'output.txt') 

BYTE_FORMAT = "<h"  # Little-Endian b
BUFF_SIZE = 1500
IP = '169.254.000.201'
PORT = 30444

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock.settimeout(1)
#sock.setblocking(False)
sock.bind(('0.0.0.0', PORT))  # works with PORT = 0 ? Heimann UDP.pdf says to set receiving port to 30444 as well

print(sock)
try:
	sock.sendto(call_msg.encode(), (IP,PORT))
	print(sock.recv(BUFF_SIZE))
	print("Connected successfully to device under %s" % IP)
	#print(sock)
	#print("here")
	#print(sock.recv(BUFF_SIZE))
	#print("there")
	#print(sock)
	#print("done")
except socket.timeout:
	sock.close()
	print("Can't connect to HTPA %s while initializing" % IP)
#print("where is it") #shows the port Rpi is receiving on

try:
	sock.sendto(bind_msg.encode(), (IP, PORT))
	print(sock.recv(BUFF_SIZE))
	print("Bound to HTPA %s" % IP)
except socket.timeout:
	self.sock.close()
	print("Failed to bind HTPA %s while initializing" % self.device.ip)
#try get a frame
try:
	sock.sendto(framereq_msg.encode(), (IP, PORT))
	print(sock.recv(BUFF_SIZE))
	print(sock.recv(BUFF_SIZE))
	print(sock.recv(BUFF_SIZE))
	#with open(output, 'a') as file:
	#	file.write(
except socket.timeout:
	sock.close()
	print("shits fucked")
#with open(output, 'a') as file:
#	file.write("test")



#sock.sendto(call.encode(),(IP,PORT))
#sock.bind((socket.gethostbyname(socket.gethostname()), 0))
#data,addr = sock.recvfrom(1500)
#print(data)
#print(sock)
'''
def decode_packets(packet1, packet2) -> str:
    """
    Decodes a pair 
    Parameters
    ----------
    packet1, packet2 : packets (buffers)
        A pair of ordered packets containing one frame captured by HTPA 32x32d.
    Returns
    -------
    str 
        Decoded space-delimited temperature values in [1e2 deg. Celsius] (consistent with Heimann's data structure)
    """
    packet = packet1 + packet2
    packet_txt = ""
    for byte in struct.iter_unpack(BYTE_FORMAT, packet):
        packet_txt += str(byte[0]) + " "
    return packet_txt
    '''
