# Light Sensor


class BH1750:
    def __init__(self, bus, address, lightlevel):
        self.bus = bus
        self.address = address

        self.adjustLight = lightlevel

        # Adjust light level (set / get)
        def set_adjustLight(self):
            return lightlevel

        def get_adjustLight(self):
            return lightlevel