import time
import smbus2

# BH1750 Address (default address is 0x23)
BH1750_ADDR = 0x23

# Power on the sensor
POWER_ON = 0x01
RESET = 0x07

# Mode setting (continuous high resolution mode)
MODE = 0x10

# Initialize the I2C bus
bus = smbus2.SMBus(1)

# Initialize the sensor
bus.write_byte(BH1750_ADDR, POWER_ON)
time.sleep(0.2)
bus.write_byte(BH1750_ADDR, RESET)
time.sleep(0.2)
bus.write_byte(BH1750_ADDR, MODE)

# Function to read the light value in lux
def read_light():
    data = bus.read_i2c_block_data(BH1750_ADDR, 0, 2)
    light_level = (data[0] << 8) + data[1]  # Combine two bytes
    lux = light_level / 1.2  # Convert to lux (as per the BH1750 datasheet)
    return lux

# Read and print the light level every 2 seconds
try:
    while True:
        lux = read_light()
        print(f"Light Level: {lux:.2f} lux")
        time.sleep(2)

except KeyboardInterrupt:
    print("Program stopped.")
