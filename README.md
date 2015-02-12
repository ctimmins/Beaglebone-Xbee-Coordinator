# Beaglebone-Xbee-Coordinator
Coordinates a network of Xbee's and uploads sensor data to Firebase

# Installation

## Firebase Data Format Sample
```javascript
/Node0 
	
	"Latitude":  '31.981',

	"Longitude": '23.111'

	"Status": "Online",

	"Sample Rate": 60 

	'2015-2-9 13:33:31': { 
		"Node": 0,
		"IR": 245,	
		"0": {
			"temp": 62,
			"vwc": 43
		},
		"1": {
			"temp": 62,
			"vwc": 43
		},
		"2": {
			"temp": 62,
			"vwc": 43
		}
	},

	'2015-2-9 13:37:22': {
		"Node": 0,
		"IR": 245,	
		"0": {
			"temp": 62,
			"vwc": 43
		},
		"1": {
			"temp": 62,
			"vwc": 43
		},
		"2": {
			"temp": 62,
			"vwc": 43
		}
	}
	
```

## USES
* Collecting data from multiple sensors
* Communicationg to multiple sensors

## Why not Digi's ConnectPort or Etherios' Device Cloud?

