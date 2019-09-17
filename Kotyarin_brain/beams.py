import RPi.GPIO as GPIO
import time
import threading

MOTOR_1_PIN = 7
BEAM_1_PIN = 13
BEAM_2_PIN = 15

class Beams_control_client ():
    def __init__(self, beam_count=2, motor_pin=MOTOR_1_PIN, beam_pins=[BEAM_1_PIN, BEAM_2_PIN], timeout=4):
        self.motor_pin = motor_pin
        self.beam_pins = beam_pins
        self.timeout = timeout
        self.end = None

    def setup(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.motor_pin, GPIO.OUT)
        for i in self.beam_pins:
            GPIO.setup(i, GPIO.IN)

        self.thread = threading.Thread(target=self.check)
        self.thread.daemon = True

        self.lock_stop_flag = threading.Lock()
        self.lock_data = threading.Lock()

        self.state = None

    def start(self):
        self.stop_flag = False
        self.end = False

        self.time_stop = time.time() + self.timeout
        GPIO.output(self.motor_pin, True)
        
        self.thread.start()

    def stop(self):
        self.thread.join()

    def check(self):
        while True:
            stop = True
            for i in self.beam_pins:
                if GPIO.input(i) == 0:
                    stop = False
                    break

            if stop or (time.time() > self.time_stop):
                GPIO.output(self.motor_pin, False)
                self.lock_data.acquire()
                self.end = True
                self.lock_data.release()
                break

    def is_ended(self):
        self.lock_data.acquire()
        state = self.end
        self.lock_data.release()
        return state

if __name__ == '__main__':
    beams = Beams_control_client()
    beams.setup()
    com = None
    while True:
        com = input()
        if (com == 'on'):
            beams.start()
            com == None
        else:
            print('State now:' + str(beams.is_ended()))
