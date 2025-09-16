import smbus2
import time

# BME280 I2C address
BME280_ADDR = 0x77  # Or 0x77 depending on your sensor's address

# Register addresses for BME280
BME280_REG_TEMP_XLSB = 0xFC
BME280_REG_TEMP_LSB = 0xFB
BME280_REG_TEMP_MSB = 0xFA
BME280_REG_PRESS_XLSB = 0xF8
BME280_REG_PRESS_LSB = 0xF7
BME280_REG_PRESS_MSB = 0xF6
BME280_REG_HUM_XLSB = 0xFD
BME280_REG_HUM_LSB = 0xFE
BME280_REG_HUM_MSB = 0xF7

# Initialize I2C (SMBus)
bus = smbus2.SMBus(1)  # '1' indicates the I2C bus on Raspberry Pi


# Function to read a 16-bit value from a register
def read_reg_16(reg):
    msb = bus.read_byte_data(BME280_ADDR, reg)
    lsb = bus.read_byte_data(BME280_ADDR, reg + 1)
    return (msb << 8) + lsb


# Function to read temperature, humidity, and pressure from BME280
def read_bme280():
    # Read raw temperature data
    temp_msb = bus.read_byte_data(BME280_ADDR, BME280_REG_TEMP_MSB)
    temp_lsb = bus.read_byte_data(BME280_ADDR, BME280_REG_TEMP_LSB)
    temp_xlsb = bus.read_byte_data(BME280_ADDR, BME280_REG_TEMP_XLSB)

    # Read raw humidity data
    hum_msb = bus.read_byte_data(BME280_ADDR, BME280_REG_HUM_MSB)
    hum_lsb = bus.read_byte_data(BME280_ADDR, BME280_REG_HUM_LSB)

    # Read raw pressure data
    press_msb = bus.read_byte_data(BME280_ADDR, BME280_REG_PRESS_MSB)
    press_lsb = bus.read_byte_data(BME280_ADDR, BME280_REG_PRESS_LSB)
    press_xlsb = bus.read_byte_data(BME280_ADDR, BME280_REG_PRESS_XLSB)

    # Combine the bytes to form the raw values
    temp_raw = (temp_msb << 12) + (temp_lsb << 4) + (temp_xlsb >> 4)
    hum_raw = (hum_msb << 8) + hum_lsb
    press_raw = (press_msb << 12) + (press_lsb << 4) + (press_xlsb >> 4)

    # Convert raw values to actual temperature, humidity, and pressure
    temperature = (
                              temp_raw / 16384.0) - 40.0  # You can adjust this based on the calibration values from the sensor datasheet
    humidity = hum_raw / 1024.0
    pressure = press_raw / 256.0

    return temperature, humidity, pressure


# Main program
try:
    while True:
        # Read sensor data
        temperature, humidity, pressure = read_bme280()

        # Print the results
        print(f"Temperature: {temperature:.2f} °C")
        print(f"Humidity: {humidity:.2f} %")
        print(f"Pressure: {pressure:.2f} hPa")

        # Wait before next reading
        time.sleep(2)

except KeyboardInterrupt:
    print("Program interrupted")

finally:
    bus.close()
