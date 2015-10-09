#UDPclient.py
#!/usr/bin/python
import socket
import sys
arglen=len(sys.argv)
if arglen<3:
    print('Ejecutar como: python cliente_udp.py <ip_address> <port>')
    exit()
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
port=8000
addr=sys.argv[1]
data=str()
data=data+sys.argv[2]
for i in range(3,len(sys.argv)):
    data=data+':'+sys.argv[i]
print data
s.sendto(data,(addr,port))
data,addr=s.recvfrom(1024)
print data
