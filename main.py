#!/usr/bin/python
from stem.stem import Stem
from time import sleep
from firebase.firebase import FirebaseApplication, FirebaseAuthentication
from userconfig import config
import binascii

if __name__ == '__main__':
	# configure firebase settings
	cf = config()
	auth = FirebaseAuthentication(cf.firebaseSecret, cf.firebaseEmail, True, True)
	fb = FirebaseApplication(cf.firebaseURL, auth)

	# defined commands FROM sensor
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

	# defined commands to SEND to sensor
	psoc_cmds = {
		'sleep':    'S',
		'resend':   'R',
		'set_rate': 'C'
	}

	# name of site for Firebase
	SITE_NAME = "Jess S. Jackson"



	stem = Stem(cmds=s_cmds)
	print '%s\n' % stem.getTime()

	while True:
		try:
			print 'waiting for frame...'
			msg = stem.xbee.wait_read_frame()
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
				stem.xbee.tx(dest_addr=msg.get('source_addr'), data='S')
			
			"""
			upload data to firebase if message type 
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
				if readType == 'soil sensors':
					print fb.put(url, timeStamp, data)
				

			
			print '--------------------------------'
			sleep(0.25)
		except KeyboardInterrupt:
			break

	if stem.serial.isOpen():
		print '\nclosing serial port from main\n'
		stem.serial.close()