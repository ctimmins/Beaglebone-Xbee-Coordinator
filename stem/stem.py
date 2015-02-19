"""
stem.py 

By Chad Timmins, 2015
chadtimmins@gmail.com 

Provides a set of functions specific to our senior design agricultural monitoring system 
"""

import serial
from xbee import XBee
from datetime import datetime
import stem_helpers as sth
import Adafruit_BBIO.UART as BB_UART

class Stem():
	def __init__(self, uart='UART2', port='/dev/ttyO2', baud=9600, cmds={}):
		# open uart port
		BB_UART.setup(uart)
		print '\n%s opened on %s\n' % (uart, port)

		# instantiate XBee and serial port objects
		self.serial = serial.Serial(port, baud)
		self.xbee = XBee(self.serial)

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
		time_stamp = self.getTime()
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
		
		print time_stamp

		# if check_sum is not valid, set command to Checksum Error
		if not sth.verifyCheckSum(check_sum):
			cmd = self.cmds.get('Cksm_Err') 

		

	def onVegRead(data):
		"""
		handles vegetronix data
		"""

	def onMLXRead(data):
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
	def handleCommand(cmd):
		try:
			if cmd == self.cmds.get('Vegetronix'):
				v_data = data[1:-1]
				self.onVegRead(v_data)
				
			elif cmd == self.cmds.get('MLX'):
				"""
				handle MLX reading
				"""
				print 'MLX reading\n'

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