#!/usr/bin/python
from xb.helpers import setup, parse
from xb.xbee import XBee
from time import sleep
from datetime import datetime
from fb.fb import FireBase



def convertIr(raw_ir=0):
	converted_ir = 0;
	return converted_ir

def getTime():
	return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':

	setup.initUart("UART2")
	
	xbee = XBee('/dev/ttyO2')

	fb = FireBase('fbUrl', 'fbEmail', 'fbSecret')

	"""
	Insert initialization code and start up tests
	"""

	while True:
		try:
			while xbee.serial.inWaiting() == 0:
				sleep(0.25)
			msg = xbee.Receive()
			try:
				msg = parse.parseXbeeMsg(msg)
				node_id = msg["SrcAddr"]
				# Get current time and date for timestamp of firebase data
				time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
				print time
				#logData(msg)
				print msg["Data"]
			except TypeError:
				print "Type Error"

			
			
				

			#xbee.SendStr(str(data), src)
			sleep(0.25)
		except KeyboardInterrupt:
			break

	xbee.serial.close()