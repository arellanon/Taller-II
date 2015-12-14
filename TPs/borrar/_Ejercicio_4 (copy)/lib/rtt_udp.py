#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket, struct, time
from sys import argv

class Rtt():
	def __init__(self):
		self.t = argv[1]		
		self.file = open('dns.txt','r')
		self.msg = struct.pack('14s','www.google.com')
		
		self.ping_avg = {}
		self.ping_min_max = {}
		self.conn = {}
		
		for ip in self.file.readlines():
			self.sent = 0
			self.received = 0
			self.lost = 0
			self.time_total_ip = 0
			self.shortest_time = 9999999
			self.longest_time = 0
			
			self.addr = ip.strip()
			self.time_exec = time.time() + int(self.t)
			
			while self.time_exec > time.time():
				self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
				self.sock.settimeout(4)
				self.sock.settimeout(10)
				self.server_address = (ip.strip(),53)
				self.start_time = time.time()
				self.sent += 1
				try:
					self.sock.sendto(self.msg, self.server_address)
					self.data = self.sock.recv(512)
					if self.data:
						self.end_time = time.time()
						self.time_total = (self.end_time - self.start_time)*1000
					if self.time_total < self.shortest_time:
						self.shortest_time = self.time_total
					if self.time_total > self.longest_time:
						self.longest_time = self.time_total
					self.time_total_ip += self.time_total
					self.received += 1
					print 'Reply from: '+str(self.addr)+' time=%.f' % self.time_total + 'ms\n'
				except:
					self.lost += 1 
					print 'unable to connect, lost package!'
					continue
			self.conn[self.addr] = (self.received,self.lost,self.sent)
			self.ping_min_max[self.addr] = (self.shortest_time,self.longest_time)
			if self.received != 0:
				self.ping_avg[self.addr] = self.time_total_ip / self.received
			else:
				self.ping_avg[self.addr] = 0
		self.file.close()
		
	def Out_Print(self):
		for addr in self.ping_min_max.keys() :
			print '-------------------------'+addr+'-------------------------'
			print 'Ping statics for '+ addr + ':'
			print 'Packets: Sent = '+str(self.conn[addr][2])+', Received = '+str(self.conn[addr][0])+', Lost = '+str(self.conn[addr][1])
			if self.ping_min_max[addr][1] == 0:
				print 
			else:
				print 'Approximate round trip times in milli-seconds: '
				print 'Minimum = %.f ' % self.ping_min_max[addr][0]+'ms, Maximum = %.f ' % self.ping_min_max[addr][1]+'ms, Average = %.f' % self.ping_avg[addr]+'ms\n'
			print '----------------------------------------------------------\n'
if __name__ == '__main__':
	rtt = Rtt()
	rtt.Out_Print()