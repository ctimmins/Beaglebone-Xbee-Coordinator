# Beaglebone-Xbee-Coordinator
Coordinates a network of Xbee's and uploads sensor data to Firebase

# Installation
*Assumes IT and other network issues have been resolved so the beaglebone has internet access*

### Install the NTP Software
* The Beaglebone needs to accurately time stamp incoming messages every time it is booted up in order to effectively upload data to Firebase.
* Follow the instructions as explained by [Derek Molloy](http://derekmolloy.ie/automatically-setting-the-beaglebone-black-time-using-ntp/)

### Install the Required Libraries and Packages
assuming `pip` is installed, save the `requirements.txt` file and run `pip install -r requirements.txt`

## Vegetronix Data Format
`input = "V,0:2.3465:22.3,1:2.0056:21.9,2:1.7319:21.8,3:1.2765:21.1,C"`

Python program splits the input wherever there are commas. `msg = input.split(",")` so the above becomes an array: 

`msg = ["V"]["0:2.3465:22.3"]["1:2.0056:21.9"]["2:1.7319:21.8"]["3:1.2765:21.1"]["C"]`

split message can be parsed for command, data, and checksum

`cmd = msg[0]`,
`cksm = msg[-1]`,
`data = msg[1:-1]`

data array is passed into `stem.onVegRead()` function and a firebase package is built accordingly.  Output of `onVegRead()` looks like: 

```javascript
"0": {
    "vwc": 2.3465,
    "temp": 22.3
},
"1": {
    "vwc": 2.0056,
    "temp": 21.9
},
"2": {
    "vwc": 1.7319,
    "temp": 21.8
},
"3": {
    "vwc": 1.2765,
    "temp": 21.1
},	
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

