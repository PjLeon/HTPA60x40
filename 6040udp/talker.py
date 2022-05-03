import socket
import os
import struct


call_msg = "Calling HTPA series devices"
bind_msg = "Bind HTPA series device"
release_msg = "x Release HTPA series device"
framereq_msg = "k"

cwd = os.getcwd()
output = os.path.join(cwd, 'output.txt') 

BYTE_FORMAT = "<h"  # Little-Endian b
BUFF_SIZE = 1500
IP = '169.254.000.201'
PORT = 30444

def decode_packet(pack):

	#packet = pack1+pack2+pack3+pack4+pack5
	packet_txt = struct.unpack('<B579h', pack)
		#packet_txt += str(byte[0]) + " "
	#with open(output, 'w') as file:
	#	file.write(packet_txt)
	print(packet_txt)
	print("shat out a frame lol")
	return packet_txt

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock.settimeout(1)
#sock.setblocking(False)
sock.bind(('0.0.0.0', PORT))  # works with PORT = 0 ? Heimann UDP.pdf says to set receiving port to 30444 as well
print(struct.calcsize('<B579h'))
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
	pack0 = sock.recv(BUFF_SIZE)
	print("got 1, length of %d"%(len(pack0)) )
	pack1 = sock.recv(BUFF_SIZE)
	print("got 2, length of %d"%(len(pack1)) )
	pack2 = sock.recv(BUFF_SIZE)
	print("got 3, length of %d"%(len(pack2)) )
	pack3 = sock.recv(BUFF_SIZE)
	print("got 4, length of %d"%(len(pack3)) )
	pack4 = sock.recv(BUFF_SIZE)
	print("got 5, length of %d"%(len(pack4)) )
	pack5 = sock.recv(BUFF_SIZE)
	print("got 6, length of %d"%(len(pack5)) )
	pack6 = sock.recv(BUFF_SIZE)
	print("got 7, length of %d"%(len(pack6)) )
	pack7 = sock.recv(BUFF_SIZE)
	print("got 8, length of %d"%(len(pack7)) )
	#with open(output, 'a') as file:
	#	file.write(
except socket.timeout:
	sock.close()
	print("shits fucked")
#with open(output, 'a') as file:
#	file.write("test")
first = decode_packet(pack2)
second = decode_packet(pack6)
diff = []
for n in range(len(first)):
	 diff.append(first[n] - second[n])
	 #print(n)
	 #print(first[n])
	 #print(second[n])

print(diff)
#sock.sendto(call.encode(),(IP,PORT))
#sock.bind((socket.gethostbyname(socket.gethostname()), 0))
#data,addr = sock.recvfrom(1500)
#print(data)
#print(sock)


