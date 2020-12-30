#!/usr/bin/env python
import RPi.GPIO as GPIO
import sys
import tty
import termios
import os
import readchar

class JGA25_370(object):

    def __init__(self, ena, in1, in2, dc_max = 100):
        self.ENA = ena
        self.IN1 = in1
        self.IN2 = in2

        self.RPM_MAX = 399
        self.DC_MAX = dc_max

        self.RPM = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)

        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)

        self.frequency = 100

        self.motorpwm = GPIO.PWM(self.ENA, self.frequency)

        self.pwm = 0

        self.motorpwm.start(0)
        self.motorpwm.ChangeDutyCycle(0)

        self.rate = 0
        self.direction = "stopped"

        self.test_speed = 0.0

    def getFrequency(self):
        return self.frequency

    def getRPMMax(self):
        return int(self.RPM_MAX)

    def getRPM(self):
        self.RPM = int((self.getRPMMax() / 2 / 60) * self.getMotorPWM())
        return self.RPM

    # alias getRPM()
    def getCurrentRPM(self):
        return self.getRPM()

    def getMaxLinearVelocity(self):
        radius_wheel = (65/2) * 0.001     # wheel radius in m
        angular_velocity = self.getRPMMax() * 0.10472   # conversion to rad/s
        linear_velocity = radius_wheel * angular_velocity * 3.6 # conversion m/s to km/h
        return linear_velocity

    # alias getMaxLinearVelocity
    def getMaxLinearVelocityKMH(self):
        return self.getMaxLinearVelocity()

    def getMaxLinearVelocityMS(self):
        return (self.getMaxLinearVelocityKMH() / 3.6)

    def getMaxLinearVelocityMPH(self):
        return (self.getMaxLinearVelocityKMH() * 0,62137)

    def getLinearVelocity(self):
        radius_wheel = (65/2) * 0.001     # wheel radius in m
        angular_velocity = self.getRPM() * 0.10472   # conversion to rad/s
        linear_velocity = radius_wheel * angular_velocity * 3.6 # conversion m/s to km/h

        if self.getMotorDirection() == 0:
            linear_velocity = 0.0
        
        if self.getMotorDirection() == "backward":
            linear_velocity = linear_velocity * -1

        return linear_velocity

    # alias getMaxLinearVelocity
    def getLinearVelocityKMH(self):
        return self.getLinearVelocity()

    def getLinearVelocityMS(self):
        linear_velocity = self.getLinearVelocityKMH() / 3.6
        return linear_velocity

    def getLinearVelocityMPH(self):
        linear_velocity = self.getLinearVelocityKMH() * 0.62137
        return linear_velocity

    def setLinearVelocity(self, linear_velocity):
        radius_wheel = (65/2) * 0.001     # wheel radius in m
        self.pwm = int(linear_velocity / (radius_wheel * 0.10472 * 3.6))

        if linear_velocity == 0:
            self.setMotorDirection("stopped")
            self.rate = 0
            self.pwm = 0
        elif linear_velocity > 0:
            self.setMotorDirection("forward")
            self.rate = self.pwm / self.DC_MAX
        elif linear_velocity < 0:
            self.setMotorDirection("backward")
            self.rate = self.pwm / self.DC_MAX * -1

        self.motorpwm.ChangeDutyCycle(self.pwm)

    def setLinearVelocityKMH(self, linear_velocity):
        radius_wheel = (65/2) * 0.001     # wheel radius in m
        self.pwm = int(linear_velocity / (radius_wheel * 0.10472 * 3.6))

        if linear_velocity == 0:
            self.setMotorDirection("stopped")
            self.rate = 0
            self.pwm = 0
        elif linear_velocity > 0:
            self.setMotorDirection("forward")
            self.rate = self.pwm / self.DC_MAX
        elif linear_velocity < 0:
            self.setMotorDirection("backward")
            self.rate = self.pwm / self.DC_MAX * -1

        self.motorpwm.ChangeDutyCycle(self.pwm)

    def setLinearVelocityMS(self, linear_velocity):
        radius_wheel = (65/2) * 0.001     # wheel radius in m
        self.pwm = int(linear_velocity / (radius_wheel * 0.10472))

        if linear_velocity == 0:
            self.setMotorDirection("stopped")
            self.rate = 0
            self.pwm = 0
        elif linear_velocity > 0:
            self.setMotorDirection("forward")
            self.rate = self.pwm / self.DC_MAX
        elif linear_velocity < 0:
            self.setMotorDirection("backward")
            self.rate = self.pwm / self.DC_MAX * -1

        self.motorpwm.ChangeDutyCycle(self.pwm)

    def setLinearVelocityMPH(self, linear_velocity):
        radius_wheel = (65/2) * 0.001     # wheel radius in m
        self.pwm = int(linear_velocity / (radius_wheel * 0.10472 * 3.6 * 0,62137))

        if linear_velocity == 0:
            self.setMotorDirection("stopped")
            self.rate = 0
            self.pwm = 0
        elif linear_velocity > 0:
            self.setMotorDirection("forward")
            self.rate = self.pwm / self.DC_MAX
        elif linear_velocity < 0:
            self.setMotorDirection("backward")
            self.rate = self.pwm / self.DC_MAX * -1

        self.motorpwm.ChangeDutyCycle(self.pwm)

    def getMotorDirection(self):
        return self.direction

    def getRate(self):
        return self.rate

    def setRate(self, rate):
        self.rate = rate

    def getDCMax(self):
        return self.DC_MAX

    def getMotorPWM(self):
        return self.pwm

    def setMotorPWM(self, pwm):
        self.pwm = pwm
    
    def setMotorDirection(self, direction):
        self.direction = direction

        if self.direction == "backward":
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
        elif self.direction == "forward":
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
        else:
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.LOW)

    def setMotorRate(self, rate):
        self.setRate(rate)

        if self.getRate() < 0:
            # reverse mode for the motor
            self.setMotorDirection("backward")
            self.setMotorPWM(-int(self.DC_MAX * self.getRate()))
            if self.getMotorPWM() > self.DC_MAX:
                self.setMotorPWM(self.DC_MAX)
        elif self.getRate() > 0:
            # forward mode for the motor
            self.setMotorDirection("forward")
            self.setMotorPWM(int(self.DC_MAX * self.getRate()))
            print(int(self.DC_MAX * self.getRate()))
            if self.getMotorPWM() > self.DC_MAX:
                self.setMotorPWM(self.DC_MAX)
        else:
            # the motor is stopped
            self.setMotorDirection("stopped")
            self.setMotorPWM(0)

        self.motorpwm.ChangeDutyCycle(self.getMotorPWM())

    def engineStop(self):
        self.setMotorDirection("stopped")
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)

        GPIO.cleanup()

    def __getch(self):
        ch = readchar.readchar()
        return ch

    def __printscreen(self):
        # The call os.system('clear') clears the screen.
        os.system('clear')
        print("w/s: forward / backward acceleration")
        print("a/d: left / right steering")
        print("q:   stopp the motors")
        print("x:   quit the program")
        print("========== Geschwindigkeitsanzeige ==========")
        print("motor speed:  ", self.test_speed)
        print("motor rate:  ", self.getRate())
        print("motor RPM: ", self.getRPM())
        print("motor PWM: ", self.getMotorPWM())
        print("======== Geschwindigkeitsanzeige II =========")
        print("speed m/s:  ", self.getLinearVelocityMS())
        print("speed km/h:  ", self.getLinearVelocityKMH())
        print("speed mp/h: ", self.getLinearVelocityMPH())

    def test_engine(self):
        while True:
            char = self.__getch()

            if(char == "w"):
                self.test_speed = self.test_speed + 0.1

                if self.test_speed > 1.0:
                    self.test_speed = 1.0

                self.setMotorRate(self.test_speed)
                self.__printscreen()

            if(char == "s"):
                self.test_speed = self.test_speed - 0.1

                if self.test_speed < -1.0:
                    self.test_speed = -1.0

                self.setMotorRate(self.test_speed)
                self.__printscreen()

            if(char == "q"):
                self.test_speed = 0.0
                self.setMotorRate(self.test_speed)
                self.__printscreen()

            if(char == "x"):
                self.setMotorRate(0.0)
                self.engineStop()
                print("Programm Ende")
                break

            char = ""
