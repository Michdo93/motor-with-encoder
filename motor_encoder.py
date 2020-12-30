import RPi.GPIO as GPIO

GPIO.setwarnings(False)

A_pin = 2  # SDA
B_pin = 3  # SCL

GPIO.setmode(GPIO.BCM)
GPIO.setup(A_pin, GPIO.IN)
GPIO.setup(B_pin, GPIO.IN)

## A | B
## 0 | 0
## 0 | 1
## 1 | 1
## 1 | 0

# PA | PB | CA | CB | Result
#  0 |  0 |  0 |  0 |  0
#  0 |  0 |  0 |  1 |  1
#  0 |  0 |  1 |  0 | -1
#  0 |  0 |  1 |  1 |  0
#  0 |  1 |  0 |  0 | -1
#  0 |  1 |  0 |  1 |  0
#  0 |  1 |  1 |  0 |  0
#  0 |  1 |  1 |  1 |  1
#  1 |  0 |  0 |  0 |  1
#  1 |  0 |  0 |  1 |  0
#  1 |  0 |  1 |  0 |  0
#  1 |  0 |  1 |  1 | -1
#  1 |  1 |  0 |  0 |  0
#  1 |  1 |  0 |  1 | -1
#  1 |  1 |  1 |  0 |  1
#  1 |  1 |  1 |  1 |  0

outcome = [0,-1,1,0,-1,0,0,1,1,0,0,-1,0,-1,1,0]
last_AB = 0b00
counter = 0

while True:
    A = GPIO.input(A_pin)
    B = GPIO.input(B_pin)
    current_AB = (A << 1) | B
    position = (last_AB << 2) | current_AB
    counter += outcome[position]
    last_AB = current_AB
    print(counter)

    ## https://www.youtube.com/watch?v=p4BCFhIuC88&t=25s

    ## https://www.youtube.com/watch?v=cLtMcqRetO0

    ## RPM = 60*(1/(time*ticks_per_rotation))
    ## time_per_rotation = time*ticks_per_rotation
    ## RPS = 1/time_per_rotation
