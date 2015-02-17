#!/usr/bin/python
from xb.helpers import setup, parse
from xb.xbee import XBee
from time import sleep
from datetime import datetime
from fb.fb import FireBase
# This is a test

"""
Data Length constants
"""
rawIRLen = 6
rawTemp = 6
rawVWC = 6

"""
Method for debugging by printing received data
"""
def logData(data={}):
	try:
		print "src: %s" % data["SrcAddr"]
		print "message length: %s" % data["MsgLen"] 
		print "Chksm: %s" % data["CheckSum"]
		print "Message: %s" % data["Data"]
	except KeyError:
		print "Missing Key"	 

def convertIr(raw_ir=0):
	converted_ir = 0;
	return converted_ir

if __name__ == '__main__':

	setup.initUart("UART2")
	
	xbee = XBee('/dev/ttyO2')

	fb = FireBase('fbUrl', 'fbEmail', 'fbSecret')

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
				logData(msg)
			except TypeError:
				print "Type Error"

			
			
				

			#xbee.SendStr(str(data), src)
			sleep(0.25)
		except KeyboardInterrupt:
			break

	xbee.serial.close()