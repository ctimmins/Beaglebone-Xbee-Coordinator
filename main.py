#!/usr/bin/python
from stem.stem import Stem
from time import sleep
from fb.fb import FireBase

if __name__ == '__main__':

	fb = FireBase('fbUrl', 'fbEmail', 'fbSecret')
	s_cmds = {
		'Vegetronix': 'V',
		'MLX':        'M',
		'Cksm_Err':   'CE',
		'Who_Am_I':   'W',
	}
	stem = Stem(cmds=s_cmds)

	while True:
		try:
			msg = stem.xbee.wait_read_frame()
			stem.onMsgReceive(msg)
			sleep(0.25)
		except KeyboardInterrupt:
			break

	if stem.serial.isOpen():
		print '\nclosing serial port from main\n'
		stem.serial.close()