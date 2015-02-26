#!/usr/bin/python
from stem.stem import Stem
from time import sleep
from firebase.firebase import FirebaseApplication, FirebaseAuthentication
from userconfig import config
if __name__ == '__main__':
	# configure firebase settings
	cf = config()
	auth = FirebaseAuthentication(cf.firebaseSecret, cf.firebaseEmail, True, True)
	fb = FirebaseApplication(cf.firebaseURL, auth)

	# defined commands
	s_cmds = {
		'Vegetronix':     'V',
		'MLX_Std':        'M',
		'MLX_Config':     'MC',
		'Cksm_Err':       'CE',
		'Who_Am_I':       'W',
	}

	stem = Stem(cmds=s_cmds)
	print stem.getTime()
	print ''
	while True:
		try:
			print 'waiting for frame...'
			msg = stem.xbee.wait_read_frame()
			res =  stem.onMsgReceive(msg)
			# source node is first element
			node = res[0]
			#data payload is second element
			data = res[1]
			readType = data['type']
			pkg = data['data']
			# get time stamp of data collection
			timeStamp = stem.getTime()
			# build URL for PUT request
			url = '%s/%s' % (node, readType)

			print fb.put(url, timeStamp, pkg)
			print ''
			sleep(0.25)
		except KeyboardInterrupt:
			break

	if stem.serial.isOpen():
		print '\nclosing serial port from main\n'
		stem.serial.close()