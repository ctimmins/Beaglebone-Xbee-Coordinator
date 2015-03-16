# Beaglebone-Xbee-Coordinator
Coordinates a network of Xbee's and uploads sensor data to Firebase

# Installation
*Assumes IT and other network issues have been resolved so the beaglebone has internet access*

### Install the NTP Software
* The Beaglebone needs to accurately time stamp incoming messages every time it is booted up in order to effectively upload data to Firebase.
* Follow the instructions as explained by [Derek Molloy](http://derekmolloy.ie/automatically-setting-the-beaglebone-black-time-using-ntp/)

### Install the Required Libraries and Packages
assuming `pip` is installed, save the `requirements.txt` file and run `pip install -r requirements.txt`

## Data Format
##### Vegetronix Sample Reading
`input = "V,0:2.3465:22.3,1:2.0056:21.9,2:1.7319:21.8,3:1.2765:21.1,C"`

Python program splits the input wherever there are commas. `msg = input.split(",")` so the above becomes an array: 

`msg = ["V"]["0:2.3465:22.3"]["1:2.0056:21.9"]["2:1.7319:21.8"]["3:1.2765:21.1"]["C"]`

split message can be parsed for command, data, and checksum

`cmd = msg[0]`,
`cksm = msg[-1]`,
`data = msg[1:-1]`

data array is passed into `stem.onVegRead()` function and a firebase package is built accordingly.  Output of `onVegRead()` looks like: 

```javascript
{
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
	}
}
```


`stem.handleCommand()` further packages the data object just received with `type` and `data` fields for easy URL building in main program.  Output of `stem.handleCommand()` looks like:

```javascript
{
	"type": "soil sensors",
	"data": {
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
		}
	}
}
```

where again the received object is packaged with the source node with an output to main like:

```javascript
{
	"source": src,
	"pkg": {
		"type": "soil sensors",
		"data": {
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
			}
		}
	}
}
```

## Main program
*Waits for incoming XBee messages to parse and upload to Firebase*
`msg = stem.xbee.wait_read_frame()`

### Building the URL for Firebase
After building a package like the one above, a URL is constructed to upload data in the correct location in Firebase. 
```python
res = stem.onMsgRecieve(msg)
node = res.get("source")
pkg = res.get("pkg")
dataType = pkg.get("type")
data = pkg.get("data")

url = '%s/%s' % (readType, node)
timeStamp = stem.getTime()

# {'print': 'silent'} header halves bandwidth of application by eliminating response back from Firebase servers
firebase.put(url, timeStamp, pkg, {'print': 'silent'})

```
Each location has top-level data fields for `node info`, `soil sensors`, and `IR readings`.  The type of command recieved from the node, will determine which of these fields the data is uploaded to.  Further, the source of the node determines where in `soil sensors` or `IR readings` the sensor data goes.

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

