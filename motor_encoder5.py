#!/usr/bin/env python3
import time
from time import sleep
import sys
import RPi.GPIO as GPIO

gpioB = 18
gpioA = 12
counter = 0

GPIO.setmode(GPIO.BOARD)
GPIO.setup(gpioA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(gpioB, GPIO.IN, pull_up_down=GPIO.PUD_UP)

Seq = [[1,0,0,1],
       [1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1]]
       
StepCount = len(Seq)
StepDir =  1# Set to 1 or 2 for clockwise
            # Set to -1 or -2 for anti-clockwise

StepCounter=0
def step_it(dir):
    global StepPins,StepCounter,angle
    StepCounter += dir
    if (StepCounter>=StepCount):
        StepCounter = 0
    if (StepCounter<0):
        StepCounter = StepCount+dir

levA = 0
levB = 0

def _callbackA(channel):
    global gpioA,gpioB,levA,levB
    level = GPIO.input(channel)
    if channel == gpioA:
        levA =level
    else:
        levB=level
    if channel == gpioA and level == 1:
        if levB == 1:
            step_it(1)
    elif channel == gpioB and level == 1:
        if levA == 1:
            step_it(-1)
angle=0

GPIO.add_event_detect(gpioA, GPIO.BOTH , _callbackA)#, bouncetime=10
GPIO.add_event_detect(gpioB, GPIO.BOTH , _callbackA)

mainloop()
