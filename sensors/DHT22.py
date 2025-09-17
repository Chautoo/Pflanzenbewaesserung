# temperature and humidity sensor

import time
import board
import adafruit_dht

class DHT22:
    def __init__(self):
        print("Initialisiere DHT22 Sensor...")

        try:
            self.dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)
        except Exception as e:
            print(f"Fehler bei der Initialisierung des Sensors: {e}")
            raise

    def read(self):
        try:
            temperature_c = self.dhtDevice.temperature
            humidity = self.dhtDevice.humidity

            if temperature_c is None or humidity is None:
                print("Sensor konnte nicht gelesen werden (None-Werte).")
                return

            temperature_f = temperature_c * (9 / 5) + 32

            print(f"Temp: {temperature_f:.1f} F / {temperature_c:.1f} C    Humidity: {humidity}%")

        except RuntimeError as error:
            print(f"Lese-Fehler: {error.args[0]}")

        except Exception as error:
            print("Kritischer Fehler, Sensor wird beendet.")
            self.dhtDevice.exit()
            raise error
