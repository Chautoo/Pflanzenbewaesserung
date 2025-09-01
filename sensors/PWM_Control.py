# PWM Control

import RPi.GPIO as GPIO


class PWM_Control:
    def __init__(self, pin, freq):
        self.pin = pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

        self.pwm = GPIO.PWM(self.pin, freq)
        self.pwm.start(0)