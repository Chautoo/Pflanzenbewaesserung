# temperature and humidity sensor


class DHT22:
    def __init__(self, pin, temp, humid):
        self.pin = pin

        self.temperature = temp
        self.humidity = humid

        # Temperature (set / get)
        def set_temperature(self):
            return temp

        def get_temperature(self):
            return temp

        # Humidity (set / get)
        def set_humidity(self):
            return humid

        def get_humidity(self):
            return humid