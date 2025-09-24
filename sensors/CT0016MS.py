# PWM Control

import requests
from gpiozero import PWMOutputDevice
import time

class CT10016MS:
    def __init__(self, gpio_pin, api_url, plant_name, temp_threshold=25.0, humidity_threshold=45.0):
        self.pump = PWMOutputDevice(gpio_pin)
        self.api_url = api_url
        self.plant_name = plant_name
        self.temp_threshold = temp_threshold
        self.humidity_threshold = humidity_threshold

    def fetch_sensor_data(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            data = response.json()
            if data.get("plant") != self.plant_name:
                print(f"Got plant: {data.get('plant')}")
                return None
            return data.get("readings", [])[-5:]  # Letzte 5 Werte
        except Exception as e:
            print(f"Error while reading the API: {e}")
            return None

    def average_values(self, readings):
        if not readings:
            return None, None
        avg_temp = sum(r["temperature"] for r in readings) / len(readings)
        avg_hum = sum(r["humidity"] for r in readings) / len(readings)
        return avg_temp, avg_hum

    def should_water(self, avg_temp, avg_hum):
        return avg_temp > self.temp_threshold and avg_hum < self.humidity_threshold

    def run_check(self):
        print("Review conditions...")
        readings = self.fetch_sensor_data()
        if readings:
            avg_temp, avg_hum = self.average_values(readings)
            print(f"Temperature: {avg_temp:.1f}°C, Humidity: {avg_hum:.1f}%")
            if self.should_water(avg_temp, avg_hum):
                self.activate_pump(duration=5)  # z.B. 5 Sekunden
            else:
                print("No watering required..")
        else:
            print("Got no valid sensor values.")

    def activate_pump(self, duration=5):
        print(f"Activated pump for {duration} seconds.")
        self.pump.value = 1.0  # 100%
        time.sleep(duration)
        self.pump.off()
        print("Pump is turned off.")

    def shutdown(self):
        self.pump.off()