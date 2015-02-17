"""
parse.py

By Chad Timmins, 2015
chadtimmins@gmail.com

Provides parsing utility functions which parses received XBee API messages
and returns a formatted data structure that can be used to retrieve
data and configuration options.

Received Messages Format: 
	[0x7E][0x00][LSB][API][SrcAddrHigh][SrcAddrLow][junk][0x00][..data..][CheckSum]

"""

def parseXbeeMsg(msg):
	# get 16-bit source address
	src = (msg[3] << 8) | msg[4]
	mlen = msg[1]
	cksm = msg[-1]
	data = msg[6:-1]

	pkg = {
		"SrcAddr": src,
		"MsgLen": mlen,
		"CheckSum": cksm,
		"Data": data
	}

	return pkg


"""
Parses data and formats for firebase uploading
"""
def parseData(msg):
	# split comma separated data portion of incoming message 
	data = msg.split(',')
	raw_ir = data[0]
	sChksm = data[-1]

	#sensor readings are the remaining data
	sdata = data[1:-1]
	fb_payload = {}
	for i in range(len(sdata)):
		sd_i = sdata[i].split(':')
		s_lev = str(i)
		fb_payload = {
			s_lev: {
				"temp": sd_i[0],
				"vwc": sd_i[1]
			}
		}

	return fb_payload
	
	#add actual IR reading to firebase package
	real_ir = convertIr(raw_ir)
	fb_payload["IR"] = real_ir

	#add node name/id to firebase package
	fb_payload["Node"] = node_id

	# send package to correct location/node in firebase
	s_location = 'Winery'
	n_url = "%s/%s" % (s_location, node_name)
	fb.put(n_url, time, fb_payload)
	


