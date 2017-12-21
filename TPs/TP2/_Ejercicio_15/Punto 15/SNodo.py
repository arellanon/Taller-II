import socket, threading, hashlib, time, os
from socket import *
from os import listdir
from os.path import isfile

class SNodo(threading.Thread):
	def __init__(self,ip,port,buffer):
		threading.Thread.__init__(self)
		self.sock = None
		self.indice = []
		self.buffer_size = int(buffer)
		self.ip = str(ip)
		self.port = int(port)
		self.listado = ''
		self.lock = threading.Lock()
		self.data = ''
		self.server_address = ''
		self.tiempo = ''
		
	def run(self):
		self.sock = socket(AF_INET, SOCK_DGRAM)
		self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		self.sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
		self.server_address = (self.ip, self.port)
		self.sock.bind(self.server_address)
		while True:
			self.data, address = self.sock.recvfrom(self.buffer_size)
			if address!= self.server_address:
				if self.data == 'listado_de_archivos_por_nodo': 
					self.indice = tareas.devolver_indice(self.ip)
					self.sendfunction(self.sock,self.indice,address)
				elif self.data == 'listado_de_archivos_completo': # se solicita emitir el listado completo
					self.listado = tareas.emitir_listado_archivos()
					self.sendfunction(self.sock,self.listado,address)
					#tareas.leer_listado_completo(self.ip)
				else:
					self.tiempo = time.time()
					tareas.listar_nodo(self.tiempo,address)
					tareas.mantener_activos()
					tareas.armar_listado_por_nodo(self.data,address)

	def sendfunction(self,sock, data, addr):
		with self.lock:
			sock.sendto(data,addr)

class Broadcast(threading.Thread):
	def __init__(self,port,time_to_broadcast):
		threading.Thread.__init__(self)
		self.time_to_broadcast = time_to_broadcast
		self.mensaje = 'listado_de_archivos_por_nodo' # intercambio de info entre nodos
		self.broadcast = '255.255.255.255'
		self.port = int(port)
		self.lock = threading.Lock()
		
	def run(self): #broadcast
		server_address = (self.broadcast, self.port)
		try:
			self.sendfunction(nodo.sock,self.mensaje,self.broadcast, self.port)
		except:
			print
		threading.Timer(int(self.time_to_broadcast), self.run).start()
		
	def sendfunction(self,sock, data, addr, port):
		with self.lock:
			sock.sendto(data,(addr,port))

class Tareas_nodo:
	def __init__(self,inactivo):
		self.inactivo = int(inactivo)
		self.mens = ''
		
	def devolver_indice(self,ip):
		self.generar_firma(ip)
		file = open('./distributed_index/'+ip+'(myself).txt','r')
		for linea in file.readlines():
			line = linea.strip("\n")
			line = line.strip(' ')
			self.mens += line+"!"
		self.mens_enviado = self.mens
		self.mens = ''
		return self.mens_enviado
	
	def generar_firma(self,ip):
		file_md5 = open('./distributed_index/'+ip+'(myself).txt','w')
		for filename in listdir('./files'):
			if isfile('./files/'+filename):
				h = hashlib.md5(open('./files/'+filename).read())
				file_md5.write(filename+" "+h.hexdigest()+"\n")
		file_md5.close()
	
	def armar_listado_por_nodo(self,data,address):
		self.data_ = data
		self.address_ = address[0]
		
		file2 = open('./distributed_index/'+self.address_+'.txt','w')
		self.data_ = self.data_.strip('!')
		self.list_file = self.data_.split('!')
		for i in self.list_file:
			e = i.strip(' ')
			f, hash_ = str(e).split(' ')
			file2.write(f+' '+hash_+' '+self.address_+'\n')
		file2.close()
	
	def emitir_listado_archivos(self):
		self.mensaje = ''
		for filename in listdir('./distributed_index'):
			if isfile('./distributed_index/'+filename) and filename.find('indice_total.txt')== -1:
				f = open('./distributed_index/'+filename,'r')
				for linea in f.readlines():
					self.mensaje += linea
				self.mensaje += '\n'
		return self.mensaje
		
	def listar_todo(self,ip):
		all_files = open('./distributed_index/indice_total.txt','w')
		for filename in listdir('./distributed_index'):
			if isfile('./distributed_index/'+filename) and filename.find('indice_total.txt')== -1:
				f = open('./distributed_index/'+filename,'r')
				if filename == (ip+'(myself).txt'):
					for i in f.readlines():
						line = i.strip('\n')
						all_files.write(line+' '+ip+'\n')
				else:
					for i in f.readlines():
						all_files.write(i)
				f.close()
		all_files.close()
	
	def leer_listado_completo(self,ip):
		self.listar_todo(ip)
		self.msg = ''
		f = open('./distributed_index/indice_total.txt','r')
		for linea in f.readlines():
			self.msg += linea+'\n'
		f.close()
		return self.msg
	
	def listar_nodo(self,tiempo, address):
		self.actualizar_tiempo = False
		if 'nodos_activos.txt' in listdir('./nodos_activos'):
			f  = open ('./nodos_activos/nodos_activos.txt','r')
			lista_nodos_activos = f.readlines()
			f.close()
			if lista_nodos_activos != []:
				for linea in lista_nodos_activos:
					line = linea.strip('\n')
					if line != '':
						ip, tiempo_ = line.split(' ')
						if ip == address[0]:
							self.actualizar_tiempo = True
							break
				if self.actualizar_tiempo == True:
					self.actualiza_tiempo(tiempo, address)
				else:
					self.agregar_al_final(tiempo, address)
			else:
				f = open ('./nodos_activos/nodos_activos.txt','a')
				f.write(str(address[0])+' '+str(tiempo)+'\n')
				f.close()
		else:
			f  = open ('./nodos_activos/nodos_activos.txt','w')
			f.write(str(address[0])+' '+str(tiempo)+'\n')
			f.close()
			
	def actualiza_tiempo(self,tiempo,address):
		f  = open ('./nodos_activos/nodos_activos.txt','r')
		lista_nodos_activos = f.readlines()
		f.close()
		f  = open ('./nodos_activos/nodos_activos.txt','w')
		for linea in lista_nodos_activos:
			line = linea.strip('\n')
			if line != '':
				ip, tiempo_ = line.split(' ')
				if ip == address[0]:
					f.write(str(address[0])+' '+str(tiempo)+'\n')
				else:
					f.write(linea)
		f.close()
	
	def agregar_al_final(self,tiempo,address):
		f  = open ('./nodos_activos/nodos_activos.txt','a')
		f.write(str(address[0])+' '+str(tiempo))
		f.close()
					
	def mantener_activos(self): # mantiene listado de nodos activos
		f = open('./nodos_activos/nodos_activos.txt','r')
		lista_nodos_activos = f.readlines()
		f.close()
		f = open('./nodos_activos/nodos_activos.txt','w')
		self.tiempo = time.time()
		for linea in lista_nodos_activos:
			if linea != '\n':
				line = linea.strip('\n')
				ip, ultima_contacto = line.split(' ')
				if (self.tiempo - float(ultima_contacto)) < self.inactivo:
					f.write(line+'\n')
				else:
					os.remove('./distributed_index/'+ip+'.txt')
					self.quitar_del_indice(ip)
		f.close()
		threading.Timer(6, self.mantener_activos).start()
	
	def quitar_del_indice(self,ip):
		f = open('./distributed_index/indice_total.txt','r')
		all_files = f.readlines()
		f.close()
		f = open('./distributed_index/indice_total.txt','w')
		for linea in all_files:
			line = linea.strip('\n')
			linea_partida = line.split(' ')
			if ip != linea_partida[-1]:
				f.write(linea)
		f.close()
		
	

class Configuracion:
	def __init__(self):
		self.diccionario = {'ip_host': '', 'port_host': 10000, 'buffer_size': 2048, 'broadcast': 5, 'tiempo_nodo_activo': 15}
	
	def setear_parametros(self):
		f = open('./config/config.cfg','r')
		for linea in f.readlines():
			line = linea.strip('\n')
			linea_partida = line.split('#')
			parametros = linea_partida[0].split('=')
			parametro = parametros[0].strip(' ')
			valor = parametros[1].strip(' ')
			self.diccionario[parametro] = valor
		return self.diccionario
		
		
if __name__ == '__main__':
	key =['ip_host','port_host','buffer_size','broadcast','tiempo_nodo_activo']
	param = []
	config = Configuracion()
	param = config.setear_parametros()
	tareas = Tareas_nodo(param[key[4]])
	nodo = SNodo(param[key[0]],param[key[1]],param[key[2]])
	nodo.start()
	broadcast = Broadcast(param[key[1]],param[key[3]])
	broadcast.start()
