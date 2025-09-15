# Light Sensor

import board
import adafruit_bh1750
import time

class BH1750:
    def __init__(self):
        self.i2c = board.I2C()  # Create once
        self.sensor = adafruit_bh1750.BH1750(self.i2c)
        time.sleep(0.1)  # Optional: wait for sensor to stabilize

    def get_value(self):
        return self.sensor.lux





