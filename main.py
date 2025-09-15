# get all classes
from sensors.BH1750 import BH1750


def readLight():
        lux = BH1750.get_value()
        print("Lux: ", lux)

# start program
if __name__ == '__main__':
    readLight()