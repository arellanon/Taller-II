import socket, argparse, sys

class ClienteUDP:
	def __init__(self,ip,port):
		self.ip = ip
		self.port = port
		self.msg = 'listado_de_archivos_completo'
		self.buffer_size = 2048
	def enviar(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		server_address = (self.ip, self.port)
		try:
			sock.sendto(self.msg, server_address)
			data, server = sock.recvfrom(self.buffer_size)
			print >>sys.stderr, '%s' % data
		except:
			print 'mensaje no enviado'
		sock.close()

if __name__== "__main__":
	parser = argparse.ArgumentParser(
        description='Solicitar listado de documentos.')
	parser.add_argument(
        '--ip',
        help='ip del nodo al que desea solicitar listado (default=127.0.0.1)', default='127.0.0.1')
	parser.add_argument(
        '--puerto', '-p',
        help='puerto donde el nodo recibe la peticion (default=5000)',
        default=5000, type=int)
	argumentos = parser.parse_args(sys.argv[1:])
	cliente = ClienteUDP(argumentos.ip, argumentos.puerto)
	cliente.enviar()