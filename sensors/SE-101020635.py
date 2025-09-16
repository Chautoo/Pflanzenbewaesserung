# Water level gauge
from RPi import GPIO


class SE101020635:
    def __init__(self):
        GPIO.setmode(10)
