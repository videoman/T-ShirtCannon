#!/usr/bin/env python 
# T-Shirt Launcher for Minnesota Roller Girls
# Using a Raspberry Pi, Darlington Transistor Array, Analog inputs for PSI (code in progress),
# and two buttoms for selecting the barrel and firing.

# David M. N. Bryan
# Attribution-NonCommercial-ShareAlike 4.0 International
#

import RPi.GPIO as GPIO
import time 
from threading import Thread
# I moved the pin assignment to another file for ease and so I chould share it with other programs
from launcher_pins import *

# This file contains the camera functions.
#from camera_includes import *

# Setup our GPIO lines
GPIO.setmode(GPIO.BCM)
# Turn off warnings...
GPIO.setwarnings(False)

# Output to the Darlington Driver for the 12V sprinkler valves
# It should be noted that these pins were choosen as they are not setup as
# on boot to be output pins.  This prevents the system from accidentdly
# firing on boot.
# Set the pull down resistor so it doesn't do bad things.
GPIO.setup(TSHIRT1, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(TSHIRT2, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(TSHIRT3, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(TSHIRT4, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)

#Setup the LED lights for outputs
GPIO.setup(LED1, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED2, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED3, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED4, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED5, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)

# Setup the Inputs
# Button one is the selector switch.
GPIO.setup(BUTTON1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Button 2 is Launcher PIN
GPIO.setup(BUTTON2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

LMODE=0
# This moves the barrel selection
def increment_lmode():
    global LMODE
    MAX_MODES=5

    # day after day, add it up!
    LMODE += 1
    if(LMODE<=0):
        LMODE=1
    elif(LMODE>=MAX_MODES):
        LMODE=1
    print('Setting launch mode to %s'%LMODE)
    light_led(LMODE)
    return(LMODE)

# Setup a t-shirt shooting function

# This is how long we hold open the solenoid
# This build now uses Toro TPV100 Series Sprinkler Valves (175PSI with 1000PSI burst)
valve_sleep_time=.1

def fireshirt(TNUMBER):
    	global F_TIME 
	global valve_sleep_time
	if (TNUMBER==1):
		TSHIRTN=TSHIRT1
		LEDN=LED1
	elif (TNUMBER==2):
		TSHIRTN=TSHIRT2
		LEDN=LED2
		# Valve 2 is a Rain Bird, and requires more time to bleed the air
		# Updated valved to Toro TPV100 valve_sleep_time=.18
	elif (TNUMBER==3):
		TSHIRTN=TSHIRT3
		LEDN=LED3
	elif (TNUMBER==4):
		TSHIRTN=TSHIRT4
		LEDN=LED4
        else:
		TSHIRTN=0

	if(ready==1): 
		# Take a picture in a thread.
		#camera_t = Thread(target=take_pictures, args=(80,LMODE))
		#thread.start_new_thread(take_pictures(10))
		#camera_t.start()

		print "Turning on valve for", valve_sleep_time, "second using pin: ", TSHIRTN
		blink_led(TNUMBER, 3, .1)

		# Turn on the Valve
        	GPIO.output(TSHIRTN, True)
        	time.sleep(valve_sleep_time)
		#Turn off the valve
        	GPIO.output(TSHIRTN, False)
    		F_TIME=time.time()

		blink_led(TNUMBER, 3, .2)
		# Turn the LED off plz
		GPIO.output(LEDN, False)
	else:
		#print "Fire command requested for", THSIRTN, " but we're not ready..."
		print('Fire button detected, but time out not yet passed: Firetime: {0} Pushtime: {1}'.format(F_TIME,time.time()))

def light_led(LED_NUM):
	if(LED_NUM==1):
		print('Turning on LED PIN: %s'%LED1)
		GPIO.output(LED1, True)	
		GPIO.output(LED2, False)	
		GPIO.output(LED3, False)	
		GPIO.output(LED4, False)	
	if(LED_NUM==2):
		print('Turning on LED PIN: %s'%LED2)
		GPIO.output(LED1, False)	
		GPIO.output(LED2, True)	
		GPIO.output(LED3, False)	
		GPIO.output(LED4, False)	
	if(LED_NUM==3):
		print('Turning on LED PIN: %s'%LED3)
		GPIO.output(LED1, False)	
		GPIO.output(LED2, False)	
		GPIO.output(LED3, True)	
		GPIO.output(LED4, False)	
	if(LED_NUM==4):
		print('Turning on LED PIN: %s'%LED4)
		GPIO.output(LED1, False)	
		GPIO.output(LED2, False)	
		GPIO.output(LED3, False)	
		GPIO.output(LED4, True)	
	if(LED_NUM==5):
		print('Turning on LED PIN: %s'%LED5)
		GPIO.output(LED5, True)	

def blink_led(LED_NUM, REPS, DELAY):
	if(LED_NUM==1):
		LEDN=LED1
	if(LED_NUM==2):
		LEDN=LED2
	if(LED_NUM==3):
		LEDN=LED3
	if(LED_NUM==4):
		LEDN=LED4
	if(LED_NUM==5):
		LEDN=LED5

	for x in range(0, REPS):
		GPIO.output(LEDN, True)
		time.sleep(DELAY)
		GPIO.output(LEDN, False)
		time.sleep(DELAY)
	
	GPIO.output(LEDN, True)

# These answer button pushes. - But with so much static in the device, this doesn't work well.
#def my_callback_sel(BUTTON1):
#	increment_lmode()

# This is an Event on push button.  It works well- but static can cause it to be pushed.
#GPIO.add_event_detect(BUTTON1, GPIO.FALLING, callback=my_callback_sel, bouncetime=200)

# This is so we can track delay times - it's not really working.
F_TIME=time.time()
ready=1

if __name__ == '__main__':
    # This is for starting up... we need to call the function to get the global variable defined
    increment_lmode()

while True:
   global ready
   time.sleep(.0005)
   if(ready==0):
	# Blink the status LED.
	blink_led(5, 5, .5)

   # Wait to see if the Fire button is being held down... 
   if(GPIO.input(BUTTON2) == 0):
	  time.sleep(.25)
	  if(GPIO.input(BUTTON2) == 0):
	 	time.sleep(.25)
		if(GPIO.input(BUTTON2) == 0):
			#my_callback_fire
			fireshirt(LMODE)
			increment_lmode()
			time.sleep(0.5)

   if(GPIO.input(BUTTON1) == 0):
      time.sleep(.005)
      if(GPIO.input(BUTTON1) == 0):
         increment_lmode()
         time.sleep(1)
