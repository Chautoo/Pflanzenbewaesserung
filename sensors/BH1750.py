# Light Sensor

import board
import busio
import adafruit_bh1750


class BH1750:
    def __init__(self):
        # I2C-Bus initialisieren
        self.i2c = busio.I2C(board.SCL, board.SDA)
        # Sensor initialisieren
        self.sensor = adafruit_bh1750.BH1750(self.i2c)

    def read_lux(self):
        # Lux-Wert lesen
        return self.sensor.lux
