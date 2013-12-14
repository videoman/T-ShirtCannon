#!/usr/bin/env python 
# T-Shirt Launcher for Minnesota Roller Girls
# Using a Raspberry Pi, Darlington Transistor Array, Analog inputs for PSI (code in progress),
# and two buttoms for selecting the barrel and firing.

# Copywrite David M. N. Bryan, all rights reserved.

import RPi.GPIO as GPIO, time

# Define our relay outputs
TSHIRT1=4
TSHIRT2=17
TSHIRT3=18
TSHIRT4=22

# Define our LED outputs
#LED1=2
#LED2=3
#LED3=14
#LED4=15
#LED5=24
LED1=2
LED2=14
LED3=3
LED4=15
LED5=24

# Define our input buttons here
#BUTTON1=27
#BUTTON2=23
BUTTON1=23
BUTTON2=27

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
GPIO.setup(BUTTON1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Setup a t-shirt shooting function
valve_sleep_time=.08

def fireshirt(TNUMBER):
    	global F_TIME 
	global valve_sleep_time
	if (TNUMBER==1):
		TSHIRTN=TSHIRT1
	elif (TNUMBER==2):
		TSHIRTN=TSHIRT2
		valve_sleep_time=.18
	elif (TNUMBER==3):
		TSHIRTN=TSHIRT3
	elif (TNUMBER==4):
		TSHIRTN=TSHIRT4
        else:
		TSHIRTN=0

	if(ready==1): 
		print "Turning on valve for", valve_sleep_time, "second using pin: ", TSHIRTN
		blink_led(TNUMBER, 3, .1)

        	GPIO.output(TSHIRTN, True)
        	time.sleep(valve_sleep_time)
        	GPIO.output(TSHIRTN, False)
    		F_TIME=time.time()

		blink_led(TNUMBER, 6, .5)
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
		GPIO.output(LED5, False)	

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

BUTTON2_P=0
def my_callback_fire(BUTTON2):
	global BUTTON2_P
	BUTTON2_P += 1
	if(BUTTON2_P<=1):
		F_TIME2 = F_TIME + 4
		ptime=time.time()
		if(F_TIME2<=ptime):
			ready=1
			print('Fireing using launch mode %s'%LMODE)
			BUTTON_P=0
			fireshirt(LMODE)
		else:
			print('Waiting for delay_time to timeout... F_TIME: {0} Current: {1}' .format(F_TIME,ptime))
			ready=0
	else:
		print('Second push detected...')
		BUTTON2_P=0

GPIO.add_event_detect(BUTTON1, GPIO.FALLING, callback=my_callback_sel, bouncetime=1000)
GPIO.add_event_detect(BUTTON2, GPIO.FALLING, callback=my_callback_fire, bouncetime=1000)
#GPIO.add_interrupt_callback(BUTTON1, my_callback_sel, edge='falling', threaded_callback=False, debounce_timeout_ms=300)
#GPIO.add_interrupt_callback(BUTTON2, my_callback_fire, edge='falling', threaded_callback=False, debounce_timeout_ms=300)

F_TIME=time.time()
ready=1

while True:
   global ready
   time.sleep(.1)
   if(ready==0):
	# Blink the status LED.
	blink_led(5, 5, .5)
   
