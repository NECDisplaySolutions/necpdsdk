#!/bin/python
# -*- coding: utf-8 -*-
"""rpi_shutdown.py - Sample script to shut down the Raspberry Pi Compute Module when the Shutdown Signal
from the NEC display goes low - signalling that power is about to be shut off.
Copy this file to a suitable location such as "“/usr/share/NEC/".
Run this script each time the system starts.

For example it can be added to the "/etc/rc.local" file. Add the following line to the "/etc/rc.local"
file before the line with the text "exit 0":
sudo python /usr/share/NEC/rpi_shutdown.py &

[Modify the above path according to the location where this file is stored]
Revision: 170322
"""

#
# Copyright (C) 2016-17 NEC Display Solutions, Ltd
# written by Will Hollingworth <whollingworth at necdisplay.com>
# See LICENSE.rst for details.
#


import RPi.GPIO as GPIO
import time
import os


# Configure with Internal pullups enabled and to read mode.
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# Perform this when the event is triggered
def Shutdown(channel):
    print "shutdown the system..."
    GPIO.cleanup()
    os.system("sudo shutdown -h now")


# Add the function to execute when the Shutdown Signal is set low
GPIO.add_event_detect(23, GPIO.FALLING, callback=Shutdown, bouncetime=100)

# Wait for an event
while 1:
    time.sleep(1)
