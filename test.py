import time
import board
import adafruit_dht
import smbus2

# Initialize the DHT22 sensor
dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

# Initialize the I2C bus (default address 0x48 for an example)
i2c_bus = smbus2.SMBus(1)  # I2C bus 1 on Raspberry Pi
i2c_address = 0x48  # Change this to the actual address of your I2C sensor

while True:
    try:
        # Read from the DHT22 sensor
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity

        print(f"Temp: {temperature_f:.1f} F / {temperature_c:.1f} C    Humidity: {humidity}%")

        # Read data from the I2C device (example: reading 2 bytes from address 0x48)
        data = i2c_bus.read_i2c_block_data(i2c_address, 0x00, 2)  # Adjust register address (0x00) as needed
        sensor_value = (data[0] << 8) + data[1]  # Combine the two bytes
        print(f"I2C Sensor Value: {sensor_value}")

    except RuntimeError as error:
        # Handle DHT22 errors
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        # Handle general errors
        dhtDevice.exit()
        i2c_bus.close()
        raise error

    time.sleep(2.0)
