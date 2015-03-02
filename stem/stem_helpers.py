def verifyCheckSum(data, cksm, cmd):
	isValid = False
	toCksm = ''
	
	if cmd == 'V':
		for level in data:
			toCksm = toCksm + level + ','
	else:
		toCksm = data[0]
	
	bb_cksm = calculateCheckSum(toCksm) % 26 + 97 
	print 'psoc cksm: %s' % cksm
	print 'bb cksm:   %s' % chr(bb_cksm)
	
	if ord(cksm) == bb_cksm:
		isValid = True

	return isValid

def calculateCheckSum(ck_str):
	return reduce(lambda x,y:x+y, map(ord, ck_str))