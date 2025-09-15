# Light Sensor

import smbus2
import time


class BH1750:
    def __init__(self):
        self.BH1750_ADDR = 0x23
        self.MODE = 0x10
        self.bus = smbus2.SMBus(1)

    def read_lux(self):
        data = self.bus.read_i2c_block_data(self.BH1750_ADDR, self.MODE, 2)
        raw = (data[0] << 8) + data[1]
        lux = raw / 1.2
        return lux
