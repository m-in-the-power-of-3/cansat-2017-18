#!/usr/bin/env python
from MSPV2 import *
from i2cdev import *
PORT = '/dev/ttyS2'
DEV_ADDRESS = 0x73


class Inav_control_client():
    CW0_DEG = 1
    CW90_DEG = 2
    CW180_DEG = 3
    CW270_DEG = 4
    CW0_DEG_FLIP = 5
    CW90_DEG_FLIP = 6
    CW180_DEG_FLIP = 7
    CW270_DEG_FLIP = 8

    def __init__(self, port):
        self.port = port

        self.accel = [None, None, None]
        self.gyro = [None, None, None]
        self.mag = [None, None, None]

        self.accel_alignment = Inav_control_client.CW0_DEG
        self.gyro_alignment = Inav_control_client.CW0_DEG
        self.mag_alignment = Inav_control_client.CW0_DEG

        self.attitude = [None, None, None]
        self.altitude = [None, None, None]

        # fix | num sat | lat |lon | alt | speed | course | hdop
        self.gps_data = [None, None, None, None, None, None, None, None]

    def setup(self):
        self.MSP = MSPV2(self.port)
        #self.update_alignment()

    def update_alignment(self):
        data = self.MSP.read_data_alignment()
        if data is None:
            return

        self.accel_alignment = data[0]
        self.gyro_alignment = data[1]
        self.mag_alignment = data[2]

    def apply_alignment(self, data, alignment):
        if alignment == Inav_control_client.CW90_DEG:
            data[0] = data[1]
            data[1] = -data[0]
            data[2] = data[2]
        elif alignment == Inav_control_client.CW180_DEG:
            data[0] = -data[0]
            data[1] = -data[1]
            data[2] = data[2]
        elif alignment == Inav_control_client.CW270_DEG:
            data[0] = -data[1]
            data[1] = data[0]
            data[2] = data[2]
        elif alignment == Inav_control_client.CW0_DEG_FLIP:
            data[0] = -data[0]
            data[1] = data[1]
            data[2] = -data[2]
        elif alignment == Inav_control_client.CW90_DEG_FLIP:
            data[0] = data[1]
            data[1] = data[0]
            data[2] = -data[2]
        elif alignment == Inav_control_client.CW180_DEG_FLIP:
            data[0] = data[0]
            data[1] = -data[1]
            data[2] = -data[2]
        elif alignment == Inav_control_client.CW270_DEG_FLIP:
            data[0] = -data[1]
            data[1] = -data[0]
            data[2] = -data[2]
        return data

    def update_data(self):
        data = self.MSP.read_data()
        if data is None:
            return

        self.accel = self.apply_alignment(data[0], self.accel_alignment)
        self.gyro = self.apply_alignment(data[1], self.gyro_alignment)
        self.mag = self.apply_alignment(data[2], self.mag_alignment)

    def update_attitude(self):
        data = self.MSP.read_attitude()
        if data is None:
            return
        self.attitude = data

    def update_altitude(self):
        data = self.MSP.read_altitude()
        if data is None:
            return
        self.altitude = data

    def update_gps_data(self):
        data = self.MSP.read_gps_data()
        if data is None:
            return
        self.gps_data = data

    def get_data(self):
        return self.accel + self.gyro + self.mag

    def get_attitude(self):
        return self.attitude

    def get_altitude(self):
        return self.altitude

    def is_gps_get_fix(self):
        if self.gps_data[0] == 0:
            return False
        else:
            return True

    def get_gps_data(self):
        return self.gps_data


class Inav_rc_i2c_control_client():
    def __init__(self, i2c_, address=DEV_ADDRESS):
        self.i2c_line = i2c_
        self.i2c_addr = address

    def setup(self):
        self.i2c_line.set_addr(self.i2c_addr)

    def cut_data(self, data):
        message = []
        for value in data:
            message.append(value % 256)
            message.append(value >> 8)
        return message

    def send_data(self, data):
        print (data)
        message = self.cut_data(data)
        self.send_message(message)

    def send_message(self, message):
        self.i2c_line.set_addr(self.i2c_addr)
        self.i2c_line.write(message)


def cut_data(data):
    message = []
    for value in data:
        message.append(value % 256)
        message.append(value >> 8)
    return message

if __name__ == '__main__':
    Uart = serial.Serial(PORT)
    Uart.baudrate = 115200
    Uart.bytesize = serial.EIGHTBITS
    Uart.parity = serial.PARITY_NONE
    Uart.stopbits = serial.STOPBITS_ONE
    Uart.timeout = 1
    Naze = Inav_control_client(Uart)
    Naze.setup()
    i2c_line = I2C(0)
    i2c_line.set_addr(0x73)
    i2c_line.set_timeout(20)
    stm = Inav_rc_i2c_control_client(i2c_line)
    stm.setup()
    while True:
        print('========================')
        #Naze.update_data()
        #Naze.update_attitude()
        #Naze.update_gps_data()
        stm.send_data([1500, 1500, 1150, 1500, 1000, 1000, 1100, 1800])
        #print(Naze.get_data())
        #print(Naze.get_attitude())
        #print(Naze.get_gps_data())

