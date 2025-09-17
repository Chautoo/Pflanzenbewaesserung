# Water Level

import smbus2
from time import sleep


class SE101020635:
    def __init__(self):

        # Grove Water Level Sensor I2C addresses
        self.SENSOR_ADDR_1 = 0x77  # First I2C address
        self.SENSOR_ADDR_2 = 0x78  # Second I2C address

        self.bus = smbus2.SMBus(1)
        self.raw_min = 500  # Value for empty tank (adjust based on calibration)
        self.raw_max = 64095  # Value for full tank (adjust based on calibration)

        # Test sensor connectivity
        #self.test_sensor_connection()

    def test_sensor_connection(self):
        """Test if the sensor is properly connected"""
        try:
            # Try reading from both addresses to see which ones respond
            print("Testing sensor connectivity...")

            for addr in [self.SENSOR_ADDR_1, self.SENSOR_ADDR_2]:
                try:
                    # Try a simple read to test connectivity
                    data = self.bus.read_i2c_block_data(addr, 0x00, 2)
                    #print(f"Address 0x{addr:02X}: Connected - Data: {data}")
                except Exception as e:
                    print(f"Address 0x{addr:02X}: No response - {e}")

        except Exception as e:
            print(f"General I2C error: {e}")

    def read_water_level_stable(self):
        """Read water level using the most stable method"""
        try:
            # Use multiple readings and filter out obvious errors
            readings = []

            for _ in range(5):
                try:
                    data = self.bus.read_i2c_block_data(self.SENSOR_ADDR_1, 0x00, 2)
                    raw = (data[0] << 8) + data[1]

                    # Filter out obvious bad readings
                    if raw > 0 and raw < 65535:  # Valid range check
                        readings.append(raw)

                except:
                    pass

                sleep(0.1)  # Short delay between readings

            if not readings:
                return None

            # Use median to avoid outliers
            readings.sort()
            if len(readings) >= 3:
                raw = readings[len(readings) // 2]  # median
            else:
                raw = sum(readings) / len(readings)  # average

            print(raw)

            # Calculate percentage
            percent = ((raw - self.raw_min) / (self.raw_max - self.raw_min)) * 100
            percent = max(0, min(percent, 100))

            print(f"Stable reading - Raw: {raw:.0f}, Percentage: {percent:.2f}%")
            return round(percent, 2)

        except Exception as e:
            print(f"Error in stable read: {e}")
            return None
