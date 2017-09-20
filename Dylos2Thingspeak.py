#!/usr/bin/env python
  

import time
import serial
import requests
import sys

if len(sys.argv) < 2:
	print "Dylos2Thingspeak accepts a single parameter, the API write key for your "
	print "Thingspeak channel as described at"
	print "https://www.mathworks.com/help/thingspeak/update-channel-feed.html"
	exit()

apikey = sys.argv[1]
print "Using api key: ", sys.argv[1]

ser = serial.Serial(
	port='/dev/ttyUSB0',
	baudrate = 9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=4000
)

thingurl='https://api.thingspeak.com/update'

while 1:
	x=ser.readline()
	print( x[:len(x)-2])
	y = x[:len(x)-2].split(",")
	print( "Small Particles: " , y[0])
	print( "Large Particles: " , y[1])
	payload = { 'api_key': apikey, 'field1': y[0], 'field2': y[1] }
	r=requests.get(thingurl,params=payload)
	print(r.url)
	print(r)


