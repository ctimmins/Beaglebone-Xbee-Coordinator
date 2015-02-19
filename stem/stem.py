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
	def __init__(self, uart='UART2', port='/dev/ttyO2', baud=9600):
		# open uart port
		BB_UART.setup(uart)
		print '%s opened on %s' % (uart, port) 
		# instantiate XBee and serial port objects
		self.serial = serial.Serial(port, baud)
		self.xbee = XBee(self.serial)
		print 'xbee instantiated'
		self.onStartup()

	def __del__(self):
		if self.serial.isOpen():
			print 'closing serial port from Class'
			self.serial.close()
	
	def getTime(self):
		return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	def onStartup(self):
		print 'onStartup function calls'

	def onMsgReceive(self, msg):
		src = msg.get('source_addr')
		if src != None:
			src = ord(src[0]) << 8 | ord(src[1])
			print 'source_addr: %s' % src
