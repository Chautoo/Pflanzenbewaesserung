# Light Sensor

import board
import busio
import adafruit_bh1750


class BH1750:
    def __init__(self):

        # I2C-Bus initialising
        self.i2c = busio.I2C(board.SCL, board.SDA)

        # Sensor initialising
        self.sensor = adafruit_bh1750.BH1750(self.i2c)

    def read_lux(self):
        # read Lux value
        return self.sensor.lux
