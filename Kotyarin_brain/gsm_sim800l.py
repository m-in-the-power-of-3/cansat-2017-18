import os
import unittest
import serial
import serial.threaded
import time
import sys

# on which port should the tests be performed:
PORT = ''

class TestLines(serial.threaded.LineReader):
    def __init__(self):
        super(TestLines, self).__init__()
        self.received_lines = []

    def handle_line(self, data):
        self.received_lines.append(data)
        GSM_notification_analyse(self.received_lines):


def GSM_notification_handle(str):
    if str.find("OK"):
        return 0
    elif str.find("CMTE "):
        pass
    elif str.find("VOLTAGE"):
        if str.find("WARNNING"):
            if str.find("OVER-"):
                pass
            elif str.find("UNDER-"):
                pass
        elif str.find("POWER DOWN"):
            pass
    elif str.find("CUSD"):
        pass
    elif str.find("CLIP"):
        pass
    elif str.find("CMTI"):
        pass
    elif str.find("RING"):
        pass
    return 1

def GSM_notification_analyse(list):
    if GSM_notification_handle(list[0]):
        list.pop(0)


if __name__ == '__main__':
  
    if len(sys.argv) > 1:
        PORT = sys.argv[1]
    sys.stdout.write("Testing port: {!r}\n".format(PORT))
    a = "0"
    ser = serial.serial_for_url(PORT, baudrate=115200, timeout=1)
    with serial.threaded.ReaderThread(ser, TestLines) as protocol:
        while True:
            a = a +"1"
            protocol.write_line('hello'+a)
            protocol.write_line('world')
            time.sleep(1)
            print protocol.received_lines

