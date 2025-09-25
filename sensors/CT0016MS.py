# PWM Control

from utils.api import LaravelAPIClient
import time
import os
from dotenv import load_dotenv


class CT10016MS():
    def __init__(self, waterlevel_min=5.0, ph_min=6.0, ph_max=7.5, client = LaravelAPIClient(env_path=".env"), env_path=".env"):
        self.waterlevel_min = waterlevel_min
        self.ph_min = ph_min
        self.ph_max = ph_max
        self.plant_id = client.getEnvValue("PLANT_ID")

        load_dotenv(dotenv_path=env_path)
        self.api_token = os.getenv("API_TOKEN")

        # prefer LaravelAPIClient config for base url if present
        try:
            self.client = LaravelAPIClient(env_path=env_path)
            self.api_url = self.client.base_url  # ensure we reuse configured base url
        except Exception:
            self.client = None  # fallback to simple requests in parent if needed

        # Define thresholds used by should_water (provide reasonable defaults)
        self.temp_threshold = 24.0
        self.humidity_threshold = 45.0

        # Initialize pump interface (stubbed for now; replace with real GPIO/PWM driver)
        class _Pump:
            def __init__(self):
                self.value = 0.0  # duty cycle 0.0 - 1.0
                self._is_on = False
            def off(self):
                self.value = 0.0
                self._is_on = False
                print("Pump off() called.")
        self.pump = _Pump()

    def fetch_sensor_data(self):
        endpoint = "measures"
        try:
            if self.client:
                data = self.client.get(endpoint)
            else:
                return super().fetch_sensor_data()

            if not data:
                return None

            print("Full data:", data)

            # Filter readings for this plant_id
            readings = [entry for entry in data if int(entry.get("plant_id", -1)) == int(self.plant_id)]

            if not readings:
                print(f"No readings found for plant_id {self.plant_id}")
                return None

            # Sort by timestamp if available, or just take last 5
            sorted_readings = sorted(readings, key=lambda x: x.get("timestamp", ""), reverse=True)
            return sorted_readings[:5]
        except Exception as e:
            print(f"Error while reading the API: {e}")
            return None

    def average_values(self, readings):
        if not readings:
            return None, None, None, None
        try:
            avg_temp = sum(r.get("temperature", 0) for r in readings) / len(readings)
            avg_hum = sum(r.get("humidity", 0) for r in readings) / len(readings)
            avg_water = sum(r.get("water_level", 0) for r in readings) / len(readings)
            avg_ph = sum(r.get("ph", 7.0) for r in readings) / len(readings)
            return avg_temp, avg_hum, avg_water, avg_ph
        except Exception:
            return None, None, None, None

    def should_water(self, avg_temp, avg_hum, avg_water, avg_ph):
        if avg_water is not None and avg_water < self.waterlevel_min:
            print(f"Water level too low ({avg_water:.1f}%), skipping watering.")
            return False
        if avg_ph is not None and not (self.ph_min <= avg_ph <= self.ph_max):
            print(f"pH value out of range ({avg_ph:.2f}), skipping watering.")
            return False
        return (avg_temp is not None and avg_hum is not None and
                avg_temp > self.temp_threshold and avg_hum < self.humidity_threshold)

    def run_check(self):
        print("Review conditions...")
        readings = self.fetch_sensor_data()
        print(readings)
        print(self.average_values(readings))
        if readings:
            avg_temp, avg_hum, avg_water, avg_ph = self.average_values(readings)
            if None in (avg_temp, avg_hum, avg_water, avg_ph):
                print("Incomplete averages, skipping.")
                return False
            print(f"Temperature: {avg_temp:.1f}°C, Humidity: {avg_hum:.1f}%, Water Level: {avg_water:.1f}%, pH: {avg_ph:.2f}")
            if self.should_water(avg_temp, avg_hum, avg_water, avg_ph):
                self.activate_pump(duration=5)
                return True
            else:
                print("No watering required..")
                return False
        else:
            print("Got no valid sensor values or API not reachable.")
            return False

    def activate_pump(self, duration=5):
        try:
            print(f"Activated pump for {duration} seconds.")
            self.pump.value = 1.0  # 100%
            time.sleep(duration)
        finally:
            # Ensure we always turn it off
            try:
                self.pump.off()
            except Exception:
                pass
            print("Pump is turned off.")

    def shutdown(self):
        # Make shutdown safe even if pump not initialized/failed
        try:
            if hasattr(self, "pump") and self.pump:
                self.pump.off()
        except Exception:
            pass