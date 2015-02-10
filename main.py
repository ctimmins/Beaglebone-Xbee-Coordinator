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
			msg = parse.parseXbeeMsg(msg)
			logData(msg)

			node_id = msg["SrcAddr"]
			
			# Get current time and date for timestamp of firebase data
			time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

			#split comma separated data portion of incoming message 
			data = msg["Data"].split(',')
			raw_ir = data[0]
			sCksm = data[-1]

			#sensor data is remaining data
			sdata = data[1:-1]
			fb_payload = {}
			for i in range(len(sdata)):
				sd_i = sdata[i].split(':')
				s_lev = str(i)
				fb_payload = {
					s_lev: {
						"Temperature": sd_i[0],
						"VWC": sd_i[1]
					}
				}

			#add actual IR reading to firebase package
			real_ir = convertIr(raw_ir)
			fb_payload["IR"] = real_ir

			#add node name/id to firebase package
			fb_payload["Node"] = node_id

			# send package to correct location/node in firebase
			s_location = 'Winery'
			n_url = "%s/%s" % (s_location, node_name)
			fb.put(n_url, time, fb_payload)
			

			#xbee.SendStr(str(data), src)
			sleep(0.25)
		except KeyboardInterrupt:
			break

	xbee.serial.close()