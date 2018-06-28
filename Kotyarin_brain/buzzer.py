import threading

import RPi.GPIO as GPIO
import time

BUZZER_PIN = 12

ON_VALUE = 2000
OFF_VALUE = 0


class Buzzer_control_client():
    def __init__(self, pin_=BUZZER_PIN):
        self.pin = pin_
        self.time_high = 0
        self.time_low = 0.02
        self.stop_flag = False

    def setup(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)

        self.thread = threading.Thread(target=self.pwm)
        self.thread.daemon = False
        self.lock_time = threading.Lock()

        self.giv_value(0)

        self.thread.start()

    def high(self):
        GPIO.output(self.pin, True)

    def low(self):
        GPIO.output(self.pin, False)

    def pwm(self):
        while True:
            if self.stop_flag:
                return

            self.lock_time.acquire()
            if (self.time_high > 0):
                self.high()
                time.sleep(self.time_high)
            self.low()
            time.sleep(self.time_low)
            self.lock_time.release()

    def giv_value(self, value):
        if (value < 0):
            value = 0
        elif (value > 2000):
            value = 2000

        self.lock_time.acquire()
        self.time_high = value / 1000000.0
        self.time_low = 0.02 - self.time_high
        self.lock_time.release()

    def on(self):
        self.giv_value(ON_VALUE)

    def off(self):
        self.giv_value(OFF_VALUE)

    def stop(self):
        self.stop_flag = True
        self.thread.join()


if __name__ == '__main__':
    buz = buzzer_control_client()
    buz.setup()
    try:
        while True:
            com = str(input())
            if (com == 'on'):
                buz.on()
            elif (com == 'off'):
                buz.off()
            time.sleep(0.1)
    except BaseException:
        buz.stop()
