# local api

import time
from threading import Thread
from fastapi import FastAPI
from pydantic import BaseModel
from gpiozero import OutputDevice

from sensors.SE101020635 import SE101020635


app = FastAPI()
isPumpActive = False
pump_thread = None


@app.get("/app/hallo")
async def root():
    return {"message": "Hello World"}


class timedPump(BaseModel):
    duration : int


class pump_activate():
    pump = OutputDevice(13)
    def activate_pump(self, duration):
        self.pump.on()
        time.sleep(duration)
        self.pump.off()

    def start_pump(self):
        global isPumpActive, pump_thread
        isPumpActive = True
        pump_thread = Thread(target=self.pump.on())
        pump_thread.start()

    def stop_pump(self):
        global isPumpActive
        isPumpActive = False
        self.pump.off()
        print("Pump stopped.")


@app.post("/pump/timed")
async def root(payload: timedPump):
    try:
        pump_activate().activate_pump(payload.duration)
        return {"message": True}
    except Exception as e:
        # Optional: log e
        return {"message": False}


class amount(BaseModel):
    amount : int


@app.post("/pump/amount")
async def root(amount: amount):
    try:
        t = amount.amount/17
        pump_activate().activate_pump(int(t))
        return {"message": True}
    except Exception as e:
        # Optional: log e
        return {"message": False}


@app.post("/pump/permanent")
async def toggle_pump():
    global isPumpActive

    try:
        if not isPumpActive:
            pump_activate().start_pump()
        else:
            pump_activate().stop_pump()
        return {"message": True, "PumpState": isPumpActive}
    except Exception as e:
        # Optional: log e
        return {"message": False, "error": str(e)}


@app.get("/water-level")
async def root():
    sensor = SE101020635()
    low, high = sensor.read_sections()
    level = sensor.compute_level(low, high, threshold=100)
    return {"message": round(level if level is not None else 0, 1)}


@app.get("/pump-state")
async def root():
    global isPumpActive
    return {"message": isPumpActive}