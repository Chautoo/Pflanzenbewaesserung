import time
from datetime import datetime

from sensors.BH1750 import BH1750
from sensors.SE101020635 import SE101020635
from sensors.MQ135 import MQ135
from sensors.DHT22 import DHT22
from sensors.CT0016MS import CT10016MS
from utils.api import LaravelAPIClient

try:
    sensor = MQ135()

    print("Starte MQ135 Messung – Strg+C zum Beenden\n")
    while True:
        data = sensor.read_all()
        print(f"Spannung: {data['voltage']:.3f} V | Rs: {data['rs']:.1f} Ω | ppm: {data['ppm']:.2f}")
        time.sleep(1)

except KeyboardInterrupt:
    print("\nMessung beendet.")
finally:
    sensor.close()