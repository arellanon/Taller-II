#UDPserver.py
#!/usr/bin/python
import socket
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(('',22222))
while True:
    data,addr=s.recvfrom(1024)
    print('Address:',addr,'Data:',data)
    mylist=list(data.split(':'))
    intlist=list()
    for i in range(0,len(mylist)):
        intlist.append(int(mylist[i]))
    intlist.sort()
    s.sendto(str(intlist),addr)
