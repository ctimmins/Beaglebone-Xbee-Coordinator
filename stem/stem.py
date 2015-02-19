"""
stem.py 

By Chad Timmins, 2015
chadtimmins@gmail.com 

Provides a set of functions specific to our senior design agricultural monitoring system 
"""

import serial
from xbee import XBee
from datetime import datetime
import Adafruit_BBIO.UART as BB_UART

class Stem():
	def __init__(self, uart='UART2', port='/dev/ttyO2', baud=9600, cmds={}):
		# open uart port
		BB_UART.setup(uart)
		print '%s opened on %s\n' % (uart, port)

		# instantiate XBee and serial port objects
		self.serial = serial.Serial(port, baud)
		self.xbee = XBee(self.serial)
		self.onStartup()

		# make data structure to hold node settings
		self.nodes = {}

	def __del__(self):
		if self.serial.isOpen():
			print 'closing serial port from Class'
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

	def parseData(self, data):
		"""
		code for parsing data 
		"""

	def updateNodeSettings(self, src):
		print 'updating node settings\n'
		"""
		this is where code for updating a node's settings goes
		"""