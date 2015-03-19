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
import numpy as np

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

		#MLX settings
                """
		self.mlx = MLX({'V_th': 0x1A68,'Kt_1': 0x5B77,'Kt_2': 0x1234})
                """
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


		# if check_sum is not valid, return empty data
		# if not stem_helpers.verifyCheckSum(data[1:-1], check_sum, cmd):
		# 	return {'source': src, 'data': None}

		# use cmd to determine next action with remaining data
		pkg = self.handleCommand(cmd, data[1:-1])
		return {'source': src, 'pkg':pkg}

	"""
	use predefined commands to handle incoming data
	"""
	def handleCommand(self, cmd, data=''):
		try:
			if cmd == self.cmds.get('Vegetronix'):
				pkg = {}
				pkg['type'] = 'soil sensors'
				pkg['data'] = self.onVegRead(data)
				return pkg
				
			elif cmd == self.cmds.get('MLX_Std'):
				"""
				handle Standard MLX reading
				"""
				print 'Standard MLX reading\n'

			elif cmd == self.cmds.get('MLX_Comp'):
				"""
				handle MLX Compensation update
				"""
				print 'MLX compensation'
				pkg = {}
				pkg['type'] = 'MLX_CONFIG'
				pkg['data'] = {}
				return pkg

			elif cmd == self.cmds.get('MLX_PTAT'):
				"""
				handle MLX PTAT 
				"""
				print 'MLX PTAT'
				pkg = {}
				pkg['type'] = 'MLX_CONFIG'
				pkg['data'] = {}
				return pkg

			elif cmd == self.cmds.get('IR_Low'):
				"""
				handle IR Frame low 
				"""
				print 'IR Low'
				pkg = {}
				pkg['type'] = 'IR Readings'
				pkg['data'] = self.onIrRead(data[0])
				
				return pkg

			elif cmd == self.cmds.get('IR_High'):
				"""
				handle IR Frame High 
				"""
				print 'IR High'
				pkg = {}
				pkg['type'] = 'IR Readings'
				pkg['data'] = self.onIrRead(data[0])

				return pkg

			elif cmd == self.cmds.get('IR_Slope'):
				"""
				handle IR Slope
				"""
				print 'IR Slope\n'

			elif cmd == self.cmds.get('IR_Sens'):
				"""
				handle IR Sensitivity 
				"""
				print 'IR Sensitivity\n'

			elif cmd == self.cmds.get('Cksm_Err'):
				""" 
				handle Check sum error
				"""
				print 'Checksum Error\n'
				return None

			elif cmd == self.cmds.get('Who_Am_I'):
				""" 
				handle Who Am I
				"""
				print 'Who Am I\n'

			elif cmd == self.cmds.get('End_Frame'):
				"""
				Handle end of frame
				"""
				print 'End of Frame'
				pkg = {}
				pkg['type'] = 'End_Frame'
				pkg['data'] = {}
				return pkg

		except IndexError:
				print 'Index Error\n'

	"""
	handles vegetronix data
	"""
	def onVegRead(self, data):
		pkg = {}
		print 'len(data): %s' % len(data)
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

	def onIrRead(self, data):
		data_arr = np.fromstring(data, dtype=np.uint16)
		return data_arr


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
