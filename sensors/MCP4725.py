# DAC Analog-Digital Converter

import RPi.GPIO as GPIO


class MCP4725:
    def __init__(self, pin):
        self.pin = pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

        self.pwm = GPIO.PWM(self.pin, 1000)
        self.pwm.start(0)