#!/usr/bin/python
from socket import *
import struct,os,time,sys

# Servidor NTP. (123 is the NTP port number).
#time_server = ('hora.rediris.es', 123)
time_server = ('pool.ntp.org', 123)

#Fecha a -> Wed May 2 15:02:44 2012 (En segundos)
#Obtener fecha actual "date +%s" y sumarle los segundos que se quieran
fecha = 1335963764

# number of seconds between NTP epoch (1900) and Unix epoch (1970).
TIME1970 = 2208988800L # Thanks to F.Lundh

client = socket( AF_INET, SOCK_DGRAM )
data = '\x1b' + 47 * ''
client.sendto(data, time_server)
data, address = client.recvfrom( 1024 )
print data
if data:
    t = struct.unpack( '!12I', data )[10]
    if t == 0:
        raise 'invalid response'
    ct = time.ctime(t - TIME1970)
#---------------------------------------------

#Fecha limite
    a = time.gmtime(fecha)
    print a
    print a.tm_year
    print a.tm_mon
    print a.tm_mday
    print a.tm_hour
    print a.tm_min
    print a.tm_sec
    
#Fecha actual
    b = time.gmtime(t - TIME1970)
    print b
    print b.tm_year
    print b.tm_mon
    print b.tm_mday
    print b.tm_hour
    print b.tm_min
    print b.tm_sec
    
#Fecha del sistema
    horaRaw = time.time()
    c = time.localtime(horaRaw)
    print c
    print c.tm_year
    print c.tm_mon
    print c.tm_mday
    print c.tm_hour
    print c.tm_min
    print c.tm_sec
    
#Comparacion fechas
    print a == b
    print a == a
else:
    raise 'no hay conexion con el servidor ntp'
