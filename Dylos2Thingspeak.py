#!/usr/bin/env python
  
import time
import datetime
import serial
import requests
import sys

if len(sys.argv) < 2:
	print "Dylos2Thingspeak requires a single parameter, the API write key for your "
	print "Thingspeak channel as described at"
	print "https://www.mathworks.com/help/thingspeak/update-channel-feed.html"
	print "and may include an optional unlabeled numerical parameter after that which is"
	print "the number of the field to write the small particle count to."
	exit()

logfilename = "Dylos2Thingspeak.log"
def LogString(outstring):
	print(outstring)
	f = open (logfilename, 'a') 
	f.write ('%s %s\n' % (datetime.datetime.now().isoformat(), outstring))
	f.close

apikey = sys.argv[1]
LogString("Using api key: " + sys.argv[1])
if(len(sys.argv) == 3):
	basefield = int(sys.argv[2])
	small_particle_field = "field%s" % (basefield)
	large_particle_field = "field%s" % (basefield+1)
else:
	small_particle_field = "field1"
	large_particle_field = "field2"

ser = serial.Serial(
	port='/dev/ttyUSB0',
	baudrate = 9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=4000
)

thingurl='https://api.thingspeak.com/update'
#datetime.datetime.now() to get the current timestamp
#add .isoformat() to get a string

DylosSerialInput = ""
retries = 1000

while 1:
	while retries > 0:
	    try:
		DylosSerialInput=ser.readline()
		retries = 10000
		break # exit retry loop
	    except Exception:
		LogString("Reading from port %s failed, waiting 1 minute and retrying" % ("ttyUSB0"))
		readfail = True
		time.sleep(60)
		retries = retries -1

	if(retries == 0):
	    LogString("Too many retries on serial, quitting")
	    exit()
	else:
	    retries = 10000
	    
	print("From dylos:" + DylosSerialInput)
	y = DylosSerialInput[:len(DylosSerialInput)-2].split(",")
	outstring = "Read Small Particles: %s, Large Particles %s" % ( y[0],y[1])
	LogString(outstring)

	payload = { 'api_key': apikey, small_particle_field : y[0], large_particle_field: y[1] }
	while retries > 0:
	    try:
		r=requests.get(thingurl,params=payload)
		retries = 10000
		outstring = "Sent to %s, response %s" % (r.url, r)
		LogString(outstring)
		break # exit retry loop
	    except Exception:
		LogString("Writing to url %s failed, waiting 1 minute and retrying" % (thingurl))
		time.sleep(60)
		retries = retries -1

	if(retries == 0):
	    LogString("Too many retries on serial, quitting")
	    exit()
	else:
	    retries = 10000
