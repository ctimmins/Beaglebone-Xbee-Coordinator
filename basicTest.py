import serial
from xbee import XBee

ser = serial.Serial('/dev/ttyO2', 9600)
xbee = XBee(ser)

while True:
	try:
		print xbee.wait_read_frame()
	except KeyboardInterrupt:
		break

ser.close()
