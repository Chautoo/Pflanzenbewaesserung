# main

from time import sleep

from sensors.BH1750 import BH1750
from sensors.SE101020635 import SE101020635
from sensors.DHT22 import DHT22
from utils.api import LaravelAPIClient


# Light Sensor
def readLight():
        lightSensor = BH1750()
        lux = lightSensor.read_lux()
        print("Lux: ", lux)

# Water Value
def water_value():
    sensor = SE101020635()
    low, high = sensor.read_sections()
    #print("Low 8 data:", low)
    #print("High 12 data:", high)
    level = sensor.compute_level(low, high, threshold=100)
    print("Water level ≈ {:.1f}%".format(level if level is not None else 0))
    sleep(2)

# temperature_humidity
def temperature_humidity():
    sensor = DHT22()
    print("Temperature:", sensor.temperature)
    print("Humidity:", sensor.humidity)

# PH Sensor
def voltage_to_ph(voltage, offset=0.0):
    """
    Convert voltage to estimated pH value.
    Assumes 2.5V = pH 7, and ~0.18V per pH step.
    """
    return 7.0 + ((2.5 - voltage) / 0.18) + offset
print("PH Value: ", voltage_to_ph(voltage=3))

# API
def api_get():
    try:
        client = LaravelAPIClient(env_path=".env")
        response = client.get("plants")
        print(response)
    except Exception as e:
        print(e)

# start program
if __name__ == '__main__':
    readLight()
    water_value()
    temperature_humidity()
    voltage_to_ph(voltage=3)
    api_get()