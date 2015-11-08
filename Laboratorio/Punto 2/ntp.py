# -*- coding: utf-8 -*-
import struct, datetime, time, sys, pytz, socket, re

TIME1970 = 2208988800L     
tz = ''

parameters = {'dd':'%d', 'mmm':'%b', 'yy':'%y', 'hh':'%H', 'mm':'%M', 'ss':'%S', 'zzz':'%Z', 'Weekday':'%A,', 'Month':'%B', 'Day':'%d', 'Year':'%Y', 'Time':'%X', 'Zone':'%Z'}

def format(data):
	global parameters
	cadena = ''
	data_= str(struct.unpack('90s',data))
	data_aux = data_.replace('\\x00','')
	data_aux2 = data_aux.replace('(\'','')
	new_data = data_aux2.replace('\',)','')
	data_list = str(new_data).split(' ')
	if 'Daytime' or 'daytime' in data_list:
		del data_list[0]
		for element in data_list:
			hora = element.split(':')
			if len(hora) > 1:
				for elem in hora:
					if elem == hora[-1]:
						cadena += parameters[elem] 
					else:
						cadena += parameters[elem] + ':'
				hora = False
			else:
				cadena += parameters[element] + ' '
	else:
		cadena = 'Parametro incorrecto'
	return cadena

def daytime(tz, cadena):
	local_zone = pytz.timezone("America/Argentina/Buenos_Aires")

	format_time = datetime.datetime.strptime(time.ctime(ntp()), "%a %b %d %H:%M:%S %Y")

	local_time = local_zone.localize(format_time)
	new_time = local_time.astimezone(tz)

	#Formato
	time_format_1 = str(new_time.strftime(cadena))
	
	return time_format_1

def ntp():
	client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM )
	data = '\x1b' + 47 * '\0'
	client.sendto( data, ( '3.ar.pool.ntp.org', 123 )) 
	data, address = client.recvfrom( 1024 )
	if data:
		print 'Response received from NTP server: ' +  str(address)
		t = struct.unpack( '!12I', data )[10]
		t -= TIME1970
	return t

def validate_input():
	zone_ = raw_input("ingrese una zona horaria valida: ")
	while zone_ not in pytz.all_timezones:
		zone_ = raw_input("ingrese una zona horaria valida: ")
	new_zone = pytz.timezone(zone_)
	return new_zone
	
def server_up(tz):
	sock = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)	
	server_address = ('127.0.0.1', 10000)
	print >>sys.stderr, '\nstarting up on %s port %s ' % server_address
	sock.bind(server_address)

	while True:
		print >>sys.stderr, 'waiting to receive parameters of DayTime \n'
		data, address = sock.recvfrom(90)
		cadena = format(data)
		print >>sys.stderr, 'received %s bytes from %s \n' % (len(data), address)
		print >>sys.stderr, 'Parameters received: %s \n' % cadena
		
		if cadena == 'Parametro incorrecto':
			sent = sock.sendto(cadena, address)
		else:
			time_requested = daytime(tz, cadena)
			print >>sys.stderr, '\n%s \n' % time_requested
			sent = sock.sendto(time_requested, address)


if __name__=='__main__':
	tz = validate_input()
	server_up(tz)
	
	
	
	
	
	