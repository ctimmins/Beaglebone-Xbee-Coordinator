"""
stem.py 

By Chad Timmins, 2015
chadtimmins@gmail.com 

Provides a set of functions specific to our senior design agricultural monitoring system 
"""

import serial
from xbee import XBee
from datetime import datetime
import stem_helpers
import Adafruit_BBIO.UART as BB_UART

class Stem():
	def __init__(self, uart='UART2', port='/dev/ttyO2', baud=9600, cmds={}):
		# open uart port
		BB_UART.setup(uart)
		print '\n%s opened on %s\n' % (uart, port)

		# instantiate XBee and serial port objects
		self.serial = serial.Serial(port, baud)
		self.xbee = XBee(self.serial, escaped=True)

		# make data structure to hold node settings
		self.nodes = {}

		# Map of commands as defined by user/client
		self.cmds = cmds 

		# Execute startup code
		self.onStartup()

	def __del__(self):
		if self.serial.isOpen():
			print '\nclosing serial port from Class\n'
			self.serial.close()
	
	def getTime(self):
		return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	def onStartup(self):
		print 'onStartup function calls'

	def onMsgReceive(self, msg):
		#time_stamp = self.getTime()
		src = msg.get('source_addr')
		if src != None:
			# left shift MSB and OR to get src value
			src = ord(src[0]) << 8 | ord(src[1])
			
			# if source is previously unknown, make new entry for node settings
			if not src in self.nodes:
				self.nodes[src] = {'name': '', 'settings': {}}
				self.updateNodeSettings(src)
				"""
				add code for reading settings
				"""
		else:
			print "something wen't seriously wrong"

		# retrieve data and parse
		data = msg.get('rf_data').split(',')
		cmd = data[0]
		check_sum = data[-1]

		# if check_sum is not valid, set command to Checksum Error
		if not stem_helpers.verifyCheckSum(check_sum):
			return self.handleCommand('CE') 

		# use cmd to determine next action with remaining data
		return self.handleCommand(src, cmd, data[1:-1])

	"""
	use predefined commands to handle incoming data
	"""
	def handleCommand(self, src, cmd, data=''):
		try:
			if cmd == self.cmds.get('Vegetronix'):
				return self.onVegRead(data)
				
			elif cmd == self.cmds.get('MLX_Std'):
				"""
				handle Standard MLX reading
				"""
				print 'Standard MLX reading\n'

			elif cmd == self.cmds.get('MLX_Config'):
				"""
				handle MLX Settings update
				"""
				print 'MLX update\n'

			elif cmd == self.cmds.get('Cksm_Err'):
				""" 
				handle Check sum error
				"""
				print 'Checksum Error\n'

			elif cmd == self.cmds.get('Who_Am_I'):
				""" 
				handle Who Am I
				"""
				print 'Who Am I\n'

		except IndexError:
				print 'Index Error\n'

	"""
	handles vegetronix data
	"""
	def onVegRead(self, data):
		pkg = {}
		# build package to be timestamped
		for i in range(len(data)):
			s_data = data[i].split(':')
			s_lev = s_data[0]
			s_vwc = s_data[1]
			s_temp = s_data[2]
			pkg[s_lev] = {
				"vwc": s_vwc,
				"temp": s_temp
			}

		return pkg

	def onMLXRead(self, data):
		"""
		handles MLX data
		"""
	
	def parseData(self, data):
		"""
		code for parsing data 
		"""

	def updateNodeSettings(self, src):
		print 'updating node settings\n'
		"""
		this is where code for updating a node's settings goes
		"""