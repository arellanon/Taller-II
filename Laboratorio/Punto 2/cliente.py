import socket
import sys, struct

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('127.0.0.1', 10000)

parameter = raw_input('')


try:
	# Send data
	print ''
	parameter2 = struct.pack('90s',parameter)
	sent = sock.sendto(parameter2, server_address)

	# Receive response
	data, server = sock.recvfrom(90)
	print >>sys.stderr, '\n"%s" \n' % data

except:
	print 'Error \n'
sock.close()