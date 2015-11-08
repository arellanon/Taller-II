import time, socket
import threading, select, wx

# Button definitions
ID_START = wx.NewId()
ID_TEXT = wx.NewId()
ID_TEXT_2 = wx.NewId()
ID_PANEL = wx.NewId()

datos_recibidos = ''
datos_enviar = ''

class Chat_Server(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.running = 1
		self.conn = None
		self.addr = None
	def run(self):
		global datos_recibidos
		HOST = '127.0.0.1'
		PORT = 5000
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((HOST,PORT))
		s.listen(1)
		self.conn, self.addr = s.accept()
		while self.running == True:
			inputready,outputready,exceptready \
			  = select.select ([self.conn],[self.conn],[])
			for input_item in inputready:
				datos_recibidos = self.conn.recv(1024)
				break
			time.sleep(0)
	def kill(self):
		self.running = 0

class Text_Input(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.running = 1
	def run(self):
		global datos_enviar
		while self.running == True:
			try:
				if datos_enviar:
					chat_server.conn.sendall(datos_enviar)
					datos_enviar = ''
			except:
				Exception
			time.sleep(0)
	def kill(self):
		self.running = 0

class MainFrame(wx.Frame):
	def __init__(self, parent, id):
		"""Create the MainFrame."""
		no_resize = wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER|wx.RESIZE_BOX|wx.MAXIMIZE_BOX)
		wx.Frame.__init__(self, parent, id, 'Thread Test',style=no_resize,size=(640,480))
		self.panel=wx.Panel(self, ID_PANEL, pos=(0,0),size=(620,369))
		self.status = wx.StaticText(self.panel, -1, '', pos=(0,100))
		wx.Button(self, ID_START, 'Send', pos=(500,370),size=(120,70))
		self.text = wx.TextCtrl(self,ID_TEXT, '', pos=(0,370),size=(500,70))
		self.text_recv = wx.TextCtrl(self,ID_TEXT_2, '', pos=(10,10),style=wx.TE_READONLY|wx.TE_MULTILINE,size=(600,345))
		
		font1 = wx.Font(16, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
			
		self.text.SetFont(font1)
		self.text_recv.SetFont(font1)
		
		self.Bind(wx.EVT_BUTTON, self.OnStart, id=ID_START)
		self.timer = wx.Timer(self, 1)
		self.timer.Start(100)
		self.Bind(wx.EVT_TIMER, self.OnResult, self.timer)

	def OnStart(self, event):
		global datos_enviar
		datos_enviar = self.text.GetValue()
		self.text_recv.write('Yo: '+datos_enviar+'\n')
		self.text.Clear()

	def OnResult(self, event):
		global datos_recibidos
		"""Show Result status."""
		if datos_recibidos:
			self.text_recv.write('El: '+datos_recibidos+'\n')
			datos_recibidos = ''

class MainApp(wx.App):
	"""Class Main App."""
	def OnInit(self):
		self.frame = MainFrame(None, -1)
		self.frame.Show(True)
		self.SetTopWindow(self.frame)
		return True

if __name__ == '__main__':
	app = MainApp(0)
	chat_server = Chat_Server()
	chat_server.start()
	text_input = Text_Input()
	text_input.start()
	app.MainLoop()