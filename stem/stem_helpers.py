def verifyCheckSum(data, cksm, cmd):
	toCksm = ''
	for level in data:
		toCksm = toCksm + level + ','
	if cmd != 'V':
		toCksm = toCksm.split(',')[0]
	
	bb_cksm = calculateCheckSum(toCksm) % 26 + 97
	print 'data: %s' % data 
	print 'psoc cksm: %s' % cksm
	print 'bb cksm:   %s' % chr(bb_cksm)
	return True

def calculateCheckSum(ck_str):
	return reduce(lambda x,y:x+y, map(ord, ck_str))