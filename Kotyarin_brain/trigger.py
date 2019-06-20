import RPi.GPIO as GPIO
import time

TRIGGER_PIN = 24


class Trigger_control_client ():
    def __init__(self, pin_=TRIGGER_PIN):
        self.pin = pin_

    def setup(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.IN)

    def read(self):
        return GPIO.input(self.pin)


if __name__ == '__main__':
    trigger = Trigger_control_client()
    trigger.setup()
    while True:
        print (trigger.read())
        time.sleep(0.1)
