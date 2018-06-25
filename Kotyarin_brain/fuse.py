import RPi.GPIO as GPIO
import time

FUSE_PIN = 7


class fuse_control_client():
    def __init__(self, pin_=FUSE_PIN):
        self.pin = pin_

    def setup(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)

    def start(self):
        GPIO.output(self.pin, True)

    def stop(self):
        GPIO.output(self.pin, False)


if __name__ == '__main__':
    fuse = fuse_control_client()
    fuse.setup()
    while True:
        com = input()
        if (com == 'on'):
            fuse.start()
        elif (com == 'off'):
            fuse.stop()
        time.sleep(0.1)
