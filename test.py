from gpiozero import OutputDevice
import time

# Create MOSFET control object for GPIO 13
pump = OutputDevice(13)


def turn_pump_on():
    """Turn the pump on"""
    pump.on()
    print("Pump ON")


def turn_pump_off():
    """Turn the pump off"""
    pump.off()
    print("Pump OFF")


def test_pump():
    """Test the pump on/off functionality"""
    print("Testing pump...")

    # Turn on for 3 seconds
    turn_pump_on()
    time.sleep(15)

    # Turn off for 2 seconds
    turn_pump_off()
    time.sleep(2)

    print("Test complete")


if __name__ == "__main__":
    try:
        test_pump()
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        turn_pump_off()  # Ensure pump is off when exiting