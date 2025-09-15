# get all classes

def main():

    # Light Sensor
    def readLight(addr):
        lightLevel = readLight(addr)
        print(format(lightLevel, '.2f') + " lux")

# start program
if __name__ == '__main__':
    main