#!/usr/bin/env python 

import RPi.GPIO as GPIO, time

# Define our relay outputs
TSHIRT1=4
TSHIRT2=17
TSHIRT3=18
TSHIRT4=22

# Define our LED outputs
LED1=2
LED2=3
LED3=14
LED4=15
LED5=24

# Define our input buttons here
BUTTON1=27
BUTTON2=23

# Setup our GPIO lines
GPIO.setmode(GPIO.BCM)

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
GPIO.setup(BUTTON1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Setup a t-shirt shooting function
valve_sleep_time=.080
def fireshirt(TNUMBER):
	if (TNUMBER==1):
		TSHIRTN=TSHIRT1
	elif (TNUMBER==2):
		TSHIRTN=TSHIRT2
	elif (TNUMBER==3):
		TSHIRTN=TSHIRT3
	elif (TNUMBER==4):
		TSHIRTN=TSHIRT4
        else:
		TSHIRTN=0
 
	print "Turning on valve for", valve_sleep_time, "second using pin: ", TSHIRTN
        GPIO.output(TSHIRTN, True)
        time.sleep(valve_sleep_time)
        GPIO.output(TSHIRTN, False)

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

LMODE=1
light_led(LMODE)
MAX_MODES=4

# These answer button pushes.
def my_callback_sel(BUTTON1):
    global LMODE
    # We have a momentary switch that we want to increment each time it's pressed, and light up LED X.
    if(LMODE<=0):
	LMODE=0
    elif(LMODE==MAX_MODES):
	LMODE=0
    LMODE += 1
    print('Setting launch mode to %s'%LMODE)
    light_led(LMODE)

F_TIME=time.time()
def my_callback_fire(BUTTON2):
    	global F_TIME 
    	ptime=time.time() 
    	F_TIME2=F_TIME
    	F_TIME2 += 4 
	if(ptime>=F_TIME2):
    		print('Fireing using launch mode %s'%LMODE)
        	fireshirt(LMODE)
    		F_TIME=time.time()
		time.sleep(1)
	else:
		print('Fire button detected, but time out not yet passed: Firetime: {0} Pushtime: {1}'.format(F_TIME,ptime))

shot_sleep=2

GPIO.add_event_detect(BUTTON1, GPIO.RISING, callback=my_callback_sel, bouncetime=300)
GPIO.add_event_detect(BUTTON2, GPIO.RISING, callback=my_callback_fire, bouncetime=200)

while True:
   time.sleep(1)
#GPIO.add_event_callback(channel, my_callback_one)
#GPIO.add_event_callback(channel, my_callback_two)
#	fireshirt(1)
#	time.sleep(shot_sleep)
#	fireshirt(2)
#	time.sleep(shot_sleep)
#	fireshirt(3)
#	time.sleep(shot_sleep)
#	fireshirt(4)
#	time.sleep(10)
