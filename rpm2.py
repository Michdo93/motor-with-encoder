#!/usr/bin/python -u
# tachfan.py - read RPM from a PC fan tachometer wired to GPIO
#
# references:
# http://electronics.stackexchange.com/questions/8295/how-to-interpret-the-output-of-a-3-pin-computer-fan-speed-sensor
# http://www.formfactors.org/developer/specs/REV1_2_Public.pdf

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

TACH = 36 # BCM 16

GPIO.setwarnings(False)
GPIO.setup(TACH, GPIO.IN, pull_up_down=GPIO.PUD_UP)

t = time.time()
def fell(n):
	global t
	dt = time.time() - t
	if dt < 0.01: return # reject spuriously short pulses

	freq = 1 / dt
	rpm = (freq / 2) * 60
	print "%.f" % (rpm,)
	t = time.time()	

GPIO.add_event_detect(TACH, GPIO.FALLING, fell)
while True: time.sleep(1e9)
