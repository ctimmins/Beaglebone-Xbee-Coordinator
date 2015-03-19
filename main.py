#!/usr/bin/python
import serial
from xbee import XBee
import Adafruit_BBIO.UART as BB_UART
from stem.stem import Stem
from time import sleep
from firebase.firebase import FirebaseApplication, FirebaseAuthentication
from userconfig import config
import binascii

"""
Location/Site of beaglebone for Firebase.  Will change based on location
"""
SITE_NAME = "Jess S Jackson"


if __name__ == '__main__':
	
	"""
	configure UART2.  BB_UART.setup() enables UART2 a.k.a. /dev/ttyO2 on Beaglebone
	"""
	BB_UART.setup('UART2')

	"""
	Instantiate xbee module with uart serial port at 9600 baud
	"""
	ser = serial.Serial('/dev/ttyO2', 9600)
	xbee = XBee(ser, escaped=True)

	"""
	configure firebase settings
	"""
	cf = config()
	auth = FirebaseAuthentication(cf.firebaseSecret, cf.firebaseEmail, True, True)
	fb = FirebaseApplication(cf.firebaseURL, auth)

	"""
	defined commands FROM sensor
	"""
	s_cmds = {
		'Vegetronix':     'V',
		'IR_Low':         'IL',
		'IR_High':        'IH',
		'IR_Sens':        'Se',
		'IR_Slope':       'Sl',
		'MLX_Std':        'M',
		'MLX_Params':     'MP',
		'MLX_Comp':       'MC',
		'Pixel_Offset':   'PO',
		'MLX_PTAT':       'Pt',
		'MLX_PTAT_Param': 'PP',
		'Cksm_Err':       'CE',
		'Who_Am_I':       'W',
		'End_Frame':      'EF'
	}

	"""
	defined commands to SEND to sensor
	"""
	psoc_cmds = {
		'sleep':    'S',
		'resend':   'R',
		'set_rate': 'C'
	}

	"""
	Instantiate Stem object and retrieve node information from Firebase
	"""
	stem = Stem(cmds=s_cmds)
	nodeInfo = fb.get(SITE_NAME, 'node info')
	nodeIterator = iter(nodeInfo)
	next(nodeIterator)
	for node in nodeIterator:
		stem.nodes[node.get('id')] = node
	print 'node info:'
	print stem.nodes
	print '%s\n' % stem.getTime()

	while True:
		try:
			print 'waiting for frame...'
			msg = xbee.wait_read_frame()
			"""
			parse incoming message and build package to send
			to firebase.
			"""
			res = stem.onMsgReceive(msg)
			node = res.get('source')

			pkg = res.get('pkg')
			readType = pkg.get('type')
			
			"""
			send command back to PSoC to go back to sleep if the 
			last message was sent from the PSoC
			"""
			if readType == 'End_Frame':
				xbee.tx(dest_addr=msg.get('source_addr'), data='S')
			
			"""
			uploads data to firebase if message type 
			is not MLX config and NOT End of Frame
			"""
			if readType != 'MLX_CONFIG' and readType != 'End_Frame':
				data = pkg.get('data')
				# get time stamp of data collection
				timeStamp = stem.getTime()
				# build URL for PUT request
				url = '%s/%s/%s' % (SITE_NAME, readType, node)
				print 'time stamp: %s' % timeStamp
				print 'url: %s' % url
				print 'pkg: %s' % data
				# only send soil readings to firebase for now...
				#if readType == 'soil sensors':
				#	print fb.put(url, timeStamp, data, params={'print':'silent'})
				

			
			print '--------------------------------'
			sleep(0.25)
		except KeyboardInterrupt:
			break

	if ser.isOpen():
		print '\nclosing serial port from main\n'
		ser.close()