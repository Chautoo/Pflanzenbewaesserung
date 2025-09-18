# water level

import smbus2

class SE101020635:
    def __init__(self, address=0x77):

        self.address = address
        self.high_addr = 0x78
        self.low_addr = 0x77
        self.bus = smbus2.SMBus(1)
        # You might need to use buffer size 8 and 12 depending which address you read from
        self.low_count = 8
        self.high_count = 12
        self.reg_config = 0x01  # guess based on community code


    def read_sections(self):
        # Read from “low” address (8 sections)
        try:
            low_data = self.bus.read_i2c_block_data(self.low_addr, self.reg_config, self.low_count)
        except Exception as e:
            low_data = None
            print(f"Error reading low 8 sections: {e}")

        # Read from “high” address (12 sections)
        try:
            high_data = self.bus.read_i2c_block_data(self.high_addr, self.reg_config, self.high_count)
        except Exception as e:
            high_data = None
            print(f"Error reading high 12 sections: {e}")

        return low_data, high_data


    def compute_level(self, low_data, high_data, threshold=100):
        """
        Count how many capacitive pads (sections) detect water.
        threshold: raw reading above which we consider “wet”
        """
        if low_data is None or high_data is None:
            return None

        touch_val = 0

        # Count pads above threshold
        for val in low_data:
            if val > threshold:
                touch_val += 1
        for val in high_data:
            if val > threshold:
                touch_val += 1

        # Convert pad count to percentage (total pads = low+high)
        total_pads = len(low_data) + len(high_data)
        percentage = (touch_val / total_pads) * 100
        return percentage
