#!/usr/bin/env python

import gammu
import sys
import os
import time


home = os.path.expanduser("~")
phone_settings = { 
		    "alcatel" : { 
			 	  #ToDo: Add Red End Key before keypresses

				  "downloadkeys"	: "]6|||||||[5[4[[|||||||||||||[|[|||||||[",\
				  "runkeys"             : "",\
				  "openkeys"		: "]8[[",\
				  "postrun"		: "",\
				  "connection"		: "test",\
				  "config"		: ".gammurc_alcatel" \
				}, \
		    "nokia":	{ "downloadkeys"	: "rjrrjrrj<jddddddddj|ddddjujj|||||||||||||||||||||j||||||||||||j",\
				  "runkeys"		: "",\
				  "openkeys"		: "rj>jujuj*m",\
				  "postrun"             : "",\
				  "connection"		: "test",\
				  "config"		: ".gammurc_nokia" \
				},\
    		    "lg":	{ "downloadkeys"	: "rr[d[[dddddd[dd[ddddd[[|]]dd[u[[||||||[||||||||",\
				  "runkeys"		: "[|||[||||[|||]|]||]||",\
				  "openkeys"		: "",\
				  "postrun"             : "rr",\
				  "connection"		: "test",\
				  "config" 		: ".gammurc_lg" \
				}\
		 }


def press_key(sm, key, time_sleep=2):
    try:
	if key == "|":
	    time.sleep(2)
	    return True
 	else:
	    sm.PressKey(key, True)
	    time_sleep = 2;
	    time.sleep(time_sleep);
	    return True
    except:
	print("Something went wrong with key: " + str(key))
	return False

if len(sys.argv) != 2:
    print 'This requires Phone argument and properties set.'
    sys.exit(1)

device = str(sys.argv[1])
print("Device:"+device+".");
try:
    config_file = phone_settings[device]["config"]
    if config_file == None or config_file == "":
        print("No config for this device : " + str(device))
        sys.exit(1)
    config_file_path = os.path.join(home, config_file)
except:
    print("No config entry for device: " + str(device))
    sys.exit(1)

if (os.path.isfile(config_file_path)):
   print("Config file: " + config_file_path + " exists.")
else:
   print("No config file : " + str(config_file_path))
   sys.exit(1)

sm = gammu.StateMachine()
sm.ReadConfig(Filename = config_file_path)
del sys.argv[1]
sm.Init()

print("Phone is connected!")

Manufacturer = sm.GetManufacturer()
Model = sm.GetModel()
IMEI = sm.GetIMEI()
Firmware = sm.GetFirmware()
print ('Phone infomation:')
print '%-15s: %s' % ('Manufacturer', Manufacturer)
print '%-15s: %s (%s)' % ('Model', Model[0], Model[1])
print '%-15s: %s' % ('IMEI', IMEI)
print '%-15s: %s' % ('Firmware', Firmware[0])
status = sm.GetBatteryCharge()

for x in status:
    if status[x] != -1:
        print "%-15s: %s" % (x, status[x])

print("Pressing keys..")
keys = phone_settings[device]["downloadkeys"]
keys = keys + phone_settings[device]["runkeys"]
if keys == None or keys == "" :
    print("No key presses specified.")
    sys.exit(1)

for key in keys:
	well=press_key(sm, key)
	if well is True:
		print(".")
	else:
		pass
		#print("Somehting went wrong with key:" + str(key))
		#sys.exit(1)

