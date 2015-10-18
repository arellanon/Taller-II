#UDPclient.py
#!/usr/bin/python
import socket
import sys
#arglen=len(sys.argv)
#if arglen<3:
#    print('Ejecutar como: python cliente_udp.py <ip_address> <data>')
#    exit()

if __name__ == '__main__':    
    if(len(sys.argv) < 3) :
        print 'Usar: python cliente_ntp.py <ip> <puerto> <formato_fecha>'
        sys.exit()
    socket_cliente=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    addr=sys.argv[1]
    port=int(sys.argv[2])
    try:
        data=sys.argv[3]
    except:
        data = "%c"
    print data    
    socket_cliente.sendto(data,(addr,port))
    data,addr=socket_cliente.recvfrom(1024)
    print data
