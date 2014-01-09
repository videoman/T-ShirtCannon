#!/usr/bin/env python 
# T-Shirt Launcher for Minnesota Roller Girls
# Using a Raspberry Pi, Darlington Transistor Array, Analog inputs for PSI (code in progress),
# and two buttoms for selecting the barrel and firing.

# Copywrite David M. N. Bryan, all rights reserved.

import RPi.GPIO as GPIO, time 
from launcher_pins import *

# Setup our GPIO lines
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Output to the Darlington Driver for the 12V sprinkler valves
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

# Setup a t-shirt shooting function
valve_sleep_time=.08

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
		valve_sleep_time=.18
	elif (TNUMBER==3):
		TSHIRTN=TSHIRT3
		LEDN=LED3
	elif (TNUMBER==4):
		TSHIRTN=TSHIRT4
		LEDN=LED4
        else:
		TSHIRTN=0

	if(ready==1): 
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

LMODE=1
light_led(LMODE)
MAX_MODES=5

def increment_lmode():
	global LMODE
	# day after day, add it up!
	LMODE += 1
	if(LMODE<=0):
		LMODE=1
	elif(LMODE>=MAX_MODES):
		LMODE=1
    	print('Setting launch mode to %s'%LMODE)
    	light_led(LMODE)

# These answer button pushes.
def my_callback_sel(BUTTON1):
	increment_lmode()

'''    global LMODE
    # We have a momentary switch that we want to increment each time it's pressed, and light up LED X.
    LMODE += 1
    if(LMODE<=0):
	LMODE=1
    elif(LMODE>=MAX_MODES):
	LMODE=1
    print('Setting launch mode to %s'%LMODE)
    light_led(LMODE)
'''

'''def button_select():
    global LMODE
    # We have a momentary switch that we want to increment each time it's pressed, and light up LED X.
    if(LMODE<=0):
	LMODE=1
    elif(LMODE>=MAX_MODES):
	LMODE=1
    LMODE += 1
    print('Setting launch mode to %s'%LMODE)
    light_led(LMODE) 
'''


# This is an Event on push button.  It works well- but static can cause it to be pushed.
GPIO.add_event_detect(BUTTON1, GPIO.FALLING, callback=my_callback_sel, bouncetime=200)
# GPIO.add_event_detect(BUTTON2, GPIO.FALLING, callback=my_callback_fire, bouncetime=1000)

F_TIME=time.time()
ready=1

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
