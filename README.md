# Beaglebone-Xbee-Coordinator
Coordinates a network of Xbee's and uploads sensor data to Firebase

# Installation
### Install the NTP Software
* The Beaglebone needs to accurately time stamp incoming messages every time it is booted up in order to effectively upload data to Firebase.
* Follow the instructions as explained by [Derek Molloy](http://derekmolloy.ie/automatically-setting-the-beaglebone-black-time-using-ntp/)
### Install the Required Libraries and Packages
assuming `pip` is installed, save the `requirements.txt` file and run `pip install -r requirements.txt`

## Firebase Data Format Sample
```javascript
{	
	"Node Info": {
		"Node 1": {
			"Battery Status": "okay",
			"Latitude": 38.53148,
			"Longitude": -121.75369,
			"Name": "Charlie",
			"Sample Rate": 4
		},
		
		"Node 2": {
			"Battery Status": "okay",
			"Latitude": 38.53148,
			"Longitude": -121.75369,
			"Name": "Charlie",
			"Sample Rate": 4
		}
	},

	"Soil Sensors" : { 
		"Node 1": {
			"2015-03-06 16:46:37": {
				"0": {
					"temp": 22.6,
					"vwc": 43.4
				},
				"1": {
					"temp": 22.6,
					"vwc": 43.4
				},
				"2": {
					"temp": 22.6,
					"vwc": 43.4
				},
				"3": {
					"temp": 22.6,
					"vwc": 43.4
				}
			},
			"2015-03-06 16:46:37": {
				"0": {
					"temp": 22.6,
					"vwc": 43.4
				},
				"1": {
					"temp": 22.6,
					"vwc": 43.4
				},
				"2": {
					"temp": 22.6,
					"vwc": 43.4
				},
				"3": {
					"temp": 22.6,
					"vwc": 43.4
				}
			},
		},
		"Node 2": {
			"2015-03-06 16:46:37": {
				"0": {
					"temp": 22.6,
					"vwc": 43.4
				},
				"1": {
					"temp": 22.6,
					"vwc": 43.4
				},
				"2": {
					"temp": 22.6,
					"vwc": 43.4
				},
				"3": {
					"temp": 22.6,
					"vwc": 43.4
				}
			},
			"2015-03-06 16:46:37": {
				"0": {
					"temp": 22.6,
					"vwc": 43.4
				},
				"1": {
					"temp": 22.6,
					"vwc": 43.4
				},
				"2": {
					"temp": 22.6,
					"vwc": 43.4
				},
				"3": {
					"temp": 22.6,
					"vwc": 43.4
				}
			},  //end snapshot
		}  //end node 2
	}  //end soil sensors
	
}
	
```

## USES
* Collecting data from multiple sensors
* Communicationg to multiple sensors

## Why not Digi's ConnectPort or Etherios' Device Cloud?

