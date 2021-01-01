from RPi import GPIO
from time import sleep

A_pin = 2
B_pin = 3

GPIO.setmode(GPIO.BCM)
GPIO.setup(A_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(B_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

counter = 0
clkLastState = GPIO.input(A_pin)

try:
        while True:
                clkState = GPIO.input(A_pin)
                if clkState != clkLastState:
                        dtState = GPIO.input(B_pin)
                        if dtState != clkState:
                                counter += 1
                        else:
                                counter -= 1
                        print(counter)
                clkLastState = clkState
                sleep(0.01)
finally:
        GPIO.cleanup()
