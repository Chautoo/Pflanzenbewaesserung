# Light Sensor

import smbus
import time


class BH1750:
    def __init__(self, bus, address, lightlevel):
        self.bus = bus
        self.address = address

        self.adjustLight = lightlevel

        DEVICE = 0x23
        POWER_DOWN = 0x00
        POWER_ON = 0x01
        RESET = 0x07
        bus = smbus.SMBus(1)

        def convertToNumber(data):
            result = (data[1] + (256 * data[0])) / 1.2
            return (result)

        def readLight(addr=DEVICE):
            data = bus.read_i2c_block_data(addr, 0x20)
            return convertToNumber(data)
