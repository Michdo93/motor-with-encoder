import RPI.GPIO as GPIO
import time
from adafruit_motorkit import MotorKit

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

stateLast = GPIO.input(17)
rotationCount = 0
stateCount = 0
stateCountTotal = 0

circ = 207 #mm
statesPerRotation = 40
distancePerStep = circ/statesPerRotation

kit = MotorKit()
kit.motor1.throttle = 0.3

try:
    while True:
        stateCurrent = GPIO.input(17)
        if stateCurrent != stateLast:
            stateLast = stateCurrent
            stateCount += 1
            stateCountTotal += 1

        if stateCount == statesPerRotation:
            rotationCount += 1
            stateCount = 0

distance = distancePerStep * stateCountTotal
    print("Distance", distance)

except KeyboardInterrupt: #CTRL+C
    kit.motor1.throttle = 0
    GPIO.cleanuo()
