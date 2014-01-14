#!/usr/bin/python
#
# David M. N. Bryan
# Attribution-NonCommercial-ShareAlike 4.0 International
#

# This file will be used to update and change the wifi setting before launching the 
# T-Shirt cannon application

import RPi.GPIO as GPIO, time
from launcher_pins import *

# Setup our GPIO lines
GPIO.setmode(GPIO.BCM)
# Turn off warnings...
GPIO.setwarnings(False)

# Setup the Inputs
# Button one is the selector switch.
GPIO.setup(BUTTON1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Button 2 is Launcher PIN
GPIO.setup(BUTTON2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Wait to see if the select button is being held down... 
if(GPIO.input(BUTTON1) == 0):
   time.sleep(.5)
   if(GPIO.input(BUTTON1) == 0):
      time.sleep(.5)
      if(GPIO.input(BUTTON1) == 0):
         # Do some wifi changes!
         time.sleep(0.5)
