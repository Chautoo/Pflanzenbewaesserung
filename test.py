#!/usr/bin/env python3
import lgpio
import time


def main():
    # GPIO Chip öffnen
    try:
        h = lgpio.gpiochip_open(4)  # Ubuntu verwendet oft Chip 4 für Pi 5
    except Exception as e:
        print(f"Fehler beim Öffnen des GPIO Chips: {e}")
        # Versuche andere Chip-Nummern
        for chip in range(5):
            try:
                h = lgpio.gpiochip_open(chip)
                print(f"GPIO Chip {chip} erfolgreich geöffnet")
                break
            except:
                continue
        else:
            print("Kein GPIO Chip gefunden")
            return

    pin = 12
    frequency = 1000

    try:
        # PWM starten mit 0% Duty Cycle
        lgpio.tx_pwm(h, pin, frequency, 0)

        print("PWM gestartet. Drücke Ctrl+C zum Beenden...")

        while True:
            # Von 0% auf 100%
            for duty in range(0, 101, 5):
                lgpio.tx_pwm(h, pin, frequency, duty)
                time.sleep(0.1)

            # Von 100% auf 0%
            for duty in range(100, -1, -5):
                lgpio.tx_pwm(h, pin, frequency, duty)
                time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nProgramm beendet")
    except Exception as e:
        print(f"Fehler: {e}")
    finally:
        lgpio.tx_pwm(h, pin, frequency, 0)  # PWM stoppen
        lgpio.gpiochip_close(h)


if __name__ == "__main__":
    main()