import socket



sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(1)
sock.bind(('0.0.0.0', 0))
IP = '169.254.000.201'
PORT = 30444
call = "Calling HTPA series devices"
BUFF_SIZE = 1500
try:
	sock.sendto(call.encode(), (IP,PORT))
	print(sock.recv(BUFF_SIZE))
	print("Connected successfully to device under %s" % IP)
except socket.timeout:
	sock.close()
	print("Can't connect to HTPA %s while initializing" % IP)
print(sock)	
#sock.sendto(call.encode(),(IP,PORT))
#sock.bind((socket.gethostbyname(socket.gethostname()), 0))
#data,addr = sock.recvfrom(1500)
#print(data)
#print(sock)
