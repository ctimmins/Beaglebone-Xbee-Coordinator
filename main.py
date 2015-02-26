#!/usr/bin/python
from stem.stem import Stem
from time import sleep
from fb.fb import FireBase

if __name__ == '__main__':

	fb = FireBase('fbUrl', 'fbEmail', 'fbSecret')
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
			print stem.onMsgReceive(msg)
			print ''
			sleep(0.25)
		except KeyboardInterrupt:
			break

	if stem.serial.isOpen():
		print '\nclosing serial port from main\n'
		stem.serial.close()