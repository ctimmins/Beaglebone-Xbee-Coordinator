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
		'sleep':  'S',
		'resend': 'R',
	}



	stem = Stem(cmds=s_cmds)
	print '%s\n' % stem.getTime()

	while True:
		try:
			print 'waiting for frame...'
			msg = stem.xbee.wait_read_frame()
			res = stem.onMsgReceive(msg)
			node = res.get('source')

			"""
			If there is an error from the checksum, send commands
			back to PSoC for retransmit
			"""
			if res.get('data') == None:
				print 'error occured: %s' % msg.get('source_addr')
				stem.xbee.tx(dest_addr=msg.get('source_addr'), data='R');
			
			else:
				data = res.get('data')
				readType = data.get('type')
				"""
				send command back to PSoC to go back to sleep if is the 
				last message sent from the PSoC
				"""
				if readType == 'End_Frame':
					stem.xbee.tx(dest_addr=msg.get('source_addr'), data='S')
				"""
				upload data to firebase if message type 
				is not MLX config and NOT End of Frame
				"""
				if readType != 'MLX_CONFIG':
					pkg = data.get('data')
					# get time stamp of data collection
					timeStamp = stem.getTime()
					# build URL for PUT request
					url = '%s/%s' % (node, readType)
					print 'time stamp: %s' % timeStamp
					print 'url: %s' % url
					print 'pkg: %s' % pkg
					#print fb.put(url, timeStamp, pkg)
					#fb.put(url, timeStamp, pkg, {'print': 'silent'})
				
				

			#print msg
			print '--------------------------------'
			sleep(0.25)
		except KeyboardInterrupt:
			break

	if stem.serial.isOpen():
		print '\nclosing serial port from main\n'
		stem.serial.close()