#!/usr/bin/env python 

import RPi.GPIO as GPIO, time

GPIO.setmode(GPIO.BCM)

TSHIRT1=4
TSHIRT2=17
TSHIRT3=18
TSHIRT4=22

valve_sleep_time=.250

GPIO.setup(TSHIRT1, GPIO.OUT)
GPIO.setup(TSHIRT2, GPIO.OUT)
GPIO.setup(TSHIRT3, GPIO.OUT)
GPIO.setup(TSHIRT4, GPIO.OUT)

def fireshirt(TNUMBER):
	if (TNUMBER=1):
		TSHIRTN=TSHIRT1
	elif (TNUMBER=2):
		TSHIRTN=TSHIRT2
	elif (TNUMBER=3):
		TSHIRTN=TSHIRT3
	elif (TNUMBER=4):
		TSHIRTN=TSHIRT4
        else 
		TSHIRTN=0
 
	print "Turning on valve for", valve_sleep_time, "second using pin: ", TNUMBER
        GPIO.output(TNUMBER, True)
        time.sleep(valve_sleep_time)
        GPIO.output(TNUMBER, False)


while True:
	fireshirt(1)
	time.sleep(10)
	fireshirt(2)
	time.sleep(10)
	fireshirt(3)
	time.sleep(10)
	fireshirt(4)
	time.sleep(120)
