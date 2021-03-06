"""
fb.py 

By Chad Timmins, 2015
chadtimmins@gmail.com 

Provides a FireBase class for easy configuration and uploading to
remote firebase database
"""

from firebase.firebase import FirebaseApplication, FirebaseAuthentication

class FireBase(object):
	
	"""
	Initializes FireBase object using user credentials
	"""
	def __init__(self, fbUrl, fbEmail, fbSecret):
		self.auth = FirebaseAuthentication(fbSecret, fbEmail, True, True)
		self.fb = FirebaseApplication(fbUrl, self.auth)

	"""
	push data to firebase
	"""
	def pushData(self, location="winery", node="0", data={}, time=0):
		url = location + "/" + node



		
