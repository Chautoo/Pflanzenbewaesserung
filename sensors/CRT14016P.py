# PH Value

import time
import struct


class CRT14016P:
    def __init__(self):

        # ADS1115 Constants
        ADS1115_ADDRESS = 0x48
        ADS1115_POINTER_CONVERSION = 0x00
        ADS1115_POINTER_CONFIG = 0x01

        # Gain for ±6.144V range
        GAIN = 0x0000  # PGA = 6.144V
        VOLTAGE_RANGE = 6.144  # Full-scale voltage

        # Config flags
        CONFIG_OS_SINGLE = 0x8000
        CONFIG_MUX = {
            0: 0x4000,  # AIN0 vs GND
            1: 0x5000,  # AIN1 vs GND
            2: 0x6000,  # AIN2 vs GND
            3: 0x7000,  # AIN3 vs GND
        }
        CONFIG_MODE_SINGLE = 0x0100
        CONFIG_DR_128SPS = 0x0080
        CONFIG_COMP_QUE_DISABLE = 0x0003

        def build_config(channel):
            """
            Build the 16-bit config register value for the given channel.
            """
            if channel not in CONFIG_MUX:
                raise ValueError("Invalid channel. Must be 0-3.")
            return (CONFIG_OS_SINGLE |
                    CONFIG_MUX[channel] |
                    GAIN |
                    CONFIG_MODE_SINGLE |
                    CONFIG_DR_128SPS |
                    CONFIG_COMP_QUE_DISABLE)

        def read_voltage_average(bus, channel=0, address=ADS1115_ADDRESS, num_samples=10, delay=0.05):
            """
            Read voltage from ADS1115 channel and average over multiple samples.
            """
            total_voltage = 0.0
            for _ in range(num_samples):
                config = build_config(channel)
                config_bytes = [(config >> 8) & 0xFF, config & 0xFF]
                bus.write_i2c_block_data(address, ADS1115_POINTER_CONFIG, config_bytes)

                time.sleep(0.01)  # Wait for conversion (ADS1115 ~8ms at 128SPS)

                raw = bus.read_i2c_block_data(address, ADS1115_POINTER_CONVERSION, 2)
                result = struct.unpack('>h', bytes(raw))[0]  # signed 16-bit big-endian

                voltage = result * VOLTAGE_RANGE / 32768.0
                total_voltage += voltage
                time.sleep(delay)

            return total_voltage / num_samples
