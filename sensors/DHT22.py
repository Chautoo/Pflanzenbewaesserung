class PChannelMosfet:
    def __init__(self, pin):
        self._led = LED(pin)

    def on(self):
        self._led.off()  # GPIO LOW -> MOSFET ON
    def off(self):
        self._led.on()   # GPIO HIGH -> MOSFET OFF
    def toggle(self):
        self._led.toggle()

from time import sleep

mosfet = PChannelMosfet(17)

try:
    while True:
        mosfet.on()  # Turn ON load
        print("P-Channel MOSFET ON")
        sleep(10)
        mosfet.off()  # Turn OFF load
        print("P-Channel MOSFET OFF")
        sleep(5)

except KeyboardInterrupt:
    print("Program stopped")
