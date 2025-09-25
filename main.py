import time
from datetime import datetime

import uvicorn

from sensors.BH1750 import BH1750
from sensors.SE101020635 import SE101020635
from sensors.MQ135 import MQ135
from sensors.DHT22 import DHT22
from sensors.CT0016MS import CT10016MS
from utils.api import LaravelAPIClient
from utils.localApi import app


# light sensor
def read_light():
    light_sensor = BH1750()
    lux = light_sensor.read_lux()
    return round(lux, 2)


# water level
def read_water_level():
    sensor = SE101020635()
    low, high = sensor.read_sections()
    level = sensor.compute_level(low, high, threshold=100)
    return round(level if level is not None else 0, 1)


# temperature / humidity
def read_temperature_humidity():
    sensor = DHT22()
    return sensor.temperature, sensor.humidity


# ph
def voltage_to_ph(voltage, offset=0.0):
    ph = 7.0 + ((2.5 - voltage) / 0.18) + offset
    return round(ph, 2)


# air quality
def air_quality():
    try:
        sensor = MQ135

        print("Starte MQ135 Messung – Strg+C zum Beenden\n")
        while True:
            data = sensor.read_all()
            print(f"Spannung: {data['voltage']:.3f} V | Rs: {data['rs']:.1f} Ω | ppm: {data['ppm']:.2f}")
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nMessung beendet.")
    finally:
        sensor.close()


# automatic watering
def pump():
    controller = CT10016MS()
    try:
        while True:
            if not controller.run_check():
                time.sleep(LaravelAPIClient(env_path=".env").getEnvValue("UPDATE_INTERVALL"))
            else:
                time.sleep(15)
    except KeyboardInterrupt:
        print("\n Stops manually.")
    finally:
        controller.shutdown()


# read from api
def api_get():
    try:
        client = LaravelAPIClient(env_path=".env")
        response = client.get("plants")

        if response and isinstance(response, list) and len(response) > 0:
            print(response)
    except Exception as e:
        print(f"Error while reaching the API: {e}")


# send to api
def api_post_sensor_data():
    try:
        # get date from sensors
        temperature, humidity = read_temperature_humidity()
        light = read_light()
        water = read_water_level()
        ph = voltage_to_ph(voltage=3)

        # API-Client initialising
        client = LaravelAPIClient(env_path=".env")

        # Data Object
        sensor_data = {
            "plant_id" : client.getEnvValue("PLANT_ID"),
            "humidity" : humidity,
            "temperature" : temperature,
            "light" : light,
            "water" : water,
            "ph" : ph,
            "air_quality" : air_quality()
        }

        # send data
        response = client.post("measures", sensor_data)
        print("Send Data...: ", response)

    except Exception as e:
        print("Error while sending data: ", e)


#


# start main
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
    while True:
        print("Start uplaod: ", datetime.now().isoformat())

        api_post_sensor_data()
        api_get()

        intervall = int(LaravelAPIClient(env_path=".env").getEnvValue("UPDATE_INTERVALL"))

        print(f"Wait {int(intervall/60)} Minutes before send data again...")
        time.sleep(intervall)

