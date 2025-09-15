# main
from sensors.BH1750 import BH1750


def readLight():
        lightSensor = BH1750()
        lux = lightSensor.get_value()
        print("Lux: ", lux)

# start program
if __name__ == '__main__':
    readLight()