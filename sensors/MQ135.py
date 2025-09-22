# Air quality sensor

import time
import math
from smbus2 import SMBus

class MQ135:
    def __init__(self, bus_number=1, address=0x48, vcc=5.0, rl=10000.0, ro_clean_air=10000.0, a=116.6020682, b=-2.769034857):
        self.bus_number = bus_number
        self.address = address
        self.vcc = vcc
        self.rl = rl
        self.ro_clean_air = ro_clean_air
        self.a = a
        self.b = b
        self.config = 0x8483  # ADS1115 Config: AIN0, gain ±4.096V, single-shot

        self.bus = SMBus(bus_number)

    def read_voltage(self):
        config_high = (self.config >> 8) & 0xFF
        config_low = self.config & 0xFF
        self.bus.write_i2c_block_data(self.address, 0x01, [config_high, config_low])
        time.sleep(0.1)

        data = self.bus.read_i2c_block_data(self.address, 0x00, 2)
        raw = (data[0] << 8) | data[1]
        if raw > 0x7FFF:
            raw -= 0x10000

        voltage = raw * 4.096 / 32768.0
        return voltage

    def calculate_rs(self, voltage):
        if voltage <= 0:
            return None
        return self.rl * (self.vcc - voltage) / voltage

    def estimate_ppm(self, rs):
        if rs is None or rs <= 0:
            return None
        ratio = rs / self.ro_clean_air
        return math.pow(ratio / self.a, 1.0 / self.b)

    def read_all(self):
        voltage = self.read_voltage()
        rs = self.calculate_rs(voltage)
        ppm = self.estimate_ppm(rs)
        return {
            "voltage": voltage,
            "rs": rs,
            "ppm": ppm
        }

    def close(self):
        self.bus.close()
