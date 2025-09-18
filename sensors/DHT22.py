# Temperature & Humidity

import board
import adafruit_dht
import time

class DHT22:
    def __init__(self, pin=board.D17):
        self.sensor = adafruit_dht.DHT22(pin, use_pulseio=False)
        self.temperature = None
        self.humidity = None
        self.read_sensor()

    def read_sensor(self):
        for _ in range(5):
            try:
                self.temperature = self.sensor.temperature
                self.humidity = self.sensor.humidity
                return
            except RuntimeError as e:
                print("RuntimeError:", e)
                time.sleep(2.0)
            except Exception as e:
                print("Unexpected error:", e)
                break
        self.sensor.exit()
