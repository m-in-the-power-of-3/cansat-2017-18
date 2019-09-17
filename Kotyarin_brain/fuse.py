import RPi.GPIO as GPIO
import time

FUSE_PIN = 15


class Fuse_control_client():
    def __init__(self, pin_=FUSE_PIN):
        self.pin = pin_

    def setup(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        self.off()

    def on(self):
        GPIO.output(self.pin, True)

    def off(self):
        GPIO.output(self.pin, False)


if __name__ == '__main__':
    fuse = Fuse_control_client()
    fuse.setup()
    while True:
        com = input()
        if (com == 'on'):
            fuse.on()
        elif (com == 'off'):
            fuse.off()
        time.sleep(0.1)
