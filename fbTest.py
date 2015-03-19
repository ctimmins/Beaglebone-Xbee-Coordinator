from datetime import datetime
import numpy as np
from userconfig import config
from firebase.firebase import FirebaseApplication, FirebaseAuthentication
import binascii

cf = config()
auth = FirebaseAuthentication(cf.firebaseSecret, 
cf.firebaseEmail, True, True)
fb = FirebaseApplication(cf.firebaseURL, auth)

