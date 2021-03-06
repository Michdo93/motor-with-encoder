from gpiozero import DigitalInputDevice
from time import sleep

class Encoder(object):
    def __init__(self, pin):
        self._value = 0

        # setup gpiozero to call increment on each when_activated
        encoder = DigitalInputDevice(pin)
        encoder.when_activated = self._increment
        encoder.when_deactivated = self._increment
        
    def reset(self):
        self._value = 0

    def _increment(self):
        self._value += 1

    @property
    def value(self):
        return self._value

e1 = Encoder(2)
e2 = Encoder(3)

#find a sample rate
while True:
    print("e1 {} e2 {}".format(e1.value, e2.value))
    sleep(0.01)
