#!/usr/bin/python
from stem.stem import Stem
from time import sleep
from fb.fb import FireBase

if __name__ == '__main__':

	fb = FireBase('fbUrl', 'fbEmail', 'fbSecret')
	stem = Stem()

	while True:
		try:
			msg = stem.xbee.wait_read_frame()
			stem.onMsgReceive(msg)
			sleep(0.25)
		except KeyboardInterrupt:
			break

	if stem.serial.isOpen():
		print 'closing serial port from main'
		stem.serial.close()