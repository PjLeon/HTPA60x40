import socket
import os

IP_MANN = '169.254.000.201'#'169.254.0.0' 
PORT = 30444
BUFF_SIZE = 1500
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('0.0.0.0', 0))
print(s)
while True:
	data, addr = s.recvfrom(BUFF_SIZE)
	print(data)
	
#socket.gethostbyname(socket.gethostname())
