from sensors.BH1750 import BH1750
from sensors.DHT22 import DHT22
from sensors.MCP4725 import MCP4725
from sensors.MP503 import MP503
from sensors.PWM_Control import PWM_Control


def main():

    # Light Sensor
    LighSensor = BH1750(1, 0x23, 1.0)
    print(LighSensor)

    # Temperature and Humidity Sensor
    DHTSensor = DHT22(4, 0x23, 0.0)
    print(DHTSensor)

    # Analog-Digital Converter
    DAC = MCP4725(17)
    print(DAC)

    # Air Quality Sensor
    AirSensor = MP503(1, 0x23, 0.0)
    print(AirSensor)

    # PWM
    PWML = PWM_Control(18, 100)
    print(PWML)


# start program
if __name__ == '__main__':
    main