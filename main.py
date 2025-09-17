# main

from sensors.BH1750 import BH1750
from sensors.SE101020635 import SE101020635
from sensors.DHT22 import DHT22
import time


# Light Sensor
def readLight():
        lightSensor = BH1750()
        lux = lightSensor.read_lux()
        print("Lux: ", lux)

# Water Value
def water():
    sensor = SE101020635()
    level = sensor.read_water_level_stable()
    print("Water Value: ", level)

def temperature_humidity():
    sensor = DHT22()
    while True:
        sensor.read()
        time.sleep(2)

# PH Sensor
def voltage_to_ph(voltage, offset=0.0):
    """
    Convert voltage to estimated pH value.
    Assumes 2.5V = pH 7, and ~0.18V per pH step.
    """
    return 7.0 + ((2.5 - voltage) / 0.18) + offset
print("PH Value: ", voltage_to_ph(voltage=3))


# start program
if __name__ == '__main__':
    readLight()
    water()
    voltage_to_ph(voltage=3.0)