#!/usr/bin/env python3
import serial
import time
import struct

class MSPV2():
    IDENT = 100
    STATUS = 101
    RAW_IMU = 102
    SERVO = 103
    MOTOR = 104
    RC = 105
    RAW_GPS = 106
    COMP_GPS = 107
    ATTITUDE = 108
    ALTITUDE = 109
    ANALOG = 110
    RC_TUNING = 111
    PID = 112
    BOX = 113
    MISC = 114
    MOTOR_PINS = 115
    BOXNAMES = 116
    PIDNAMES = 117
    WP = 118
    BOXIDS = 119
    RC_RAW_IMU = 121
    SET_RAW_RC = 200
    SET_RAW_GPS = 201
    SET_PID = 202
    SET_BOX = 203
    SET_RC_TUNING = 204
    ACC_CALIBRATION = 205
    MAG_CALIBRATION = 206
    SET_MISC = 207
    RESET_CONF = 208
    SET_WP = 209
    SWITCH_RC_SERIAL = 210
    IS_SERIAL = 211
    DEBUG = 254
    SENSOR_ALIGNMENT = 126

    def __init__(self, port):
        self.uart = port

    def _crc8_dvb_s2(self, crc, a):
        crc ^= a
        for i in range(8):
            if (crc & 0x80):
                crc = ((crc << 1) ^ 0xD5) % 256
            else:
                crc = (crc << 1) % 256
        return crc

    def send_comand(self, data_size, code, data):
        packet = ['$', 'X', '<', 0, code, data_size] + data

        checksum = 0
        for i in struct.pack('<B2H%dH' % len(data), *packet[3:len(packet)]):
            checksum = self._crc8_dvb_s2(checksum, i)
        packet.append(checksum)

        for i in range(len(packet)):
            if isinstance(packet[i], str):
                packet[i] = packet[i].encode("utf-8")

        self.uart.write(struct.pack('<3cB2H%dHB' % len(data), *packet))

    def request_packet(self, cmd):
        self.send_comand(0, cmd, [])
        repeat = 0
        while True:
            if repeat >= 5:
                return []
            byte = self.uart.read()
            if byte == '$'.encode("utf-8"):
                break
            repeat += 1

        data = [byte]
        end = ''.encode("utf-8")
        while True:
            byte = self.uart.read()
            if byte is end:
                break
            data.append(byte)
        return data

    def unpack_packet(self, data, form):
        if len(data) < 1:
            return []

        checksum = 0
        for i in data[3:-1]:
            i = struct.unpack('<b', i)[0]
            checksum = self._crc8_dvb_s2(checksum, i)

        if struct.pack('<B', checksum) != data[-1]:
            raise IOError('MSPv2_checksum')

        unpacked_data = data[8]
        for i in data[9:-1]:
            unpacked_data += i

        unpacked_data = struct.unpack('<' + form, unpacked_data)
        return list(unpacked_data)

    def read_data(self):
        data = self.unpack_packet(self.request_packet(MSPV2.RAW_IMU), '9h')
        if len(data) < 9:
            return None
        accel = []
        for i in data[:3]:
            accel.append(i / 512.0)
        gyro = []
        for i in data[3:6]:
            gyro.append(i * (4.0 / 16.4))
        mag = []
        for i in data[6:9]:
            mag.append(i / 1090.0)

        return [accel, gyro, mag]

    def read_data_alignment(self):
        data = self.unpack_packet(self.request_packet(MSPV2.SENSOR_ALIGNMENT), '4B')
        if len(data) < 4:
            return None
        return data[:-1]

    def read_attitude(self):
        data = self.unpack_packet(self.request_packet(MSPV2.ATTITUDE), '3h')
        if len(data) < 3:
            return None
        roll = data[0] / 10.0  # крен
        pitch = data[1] / 10.0  # тангаж
        yaw = data[2]  # рысканье

        return [roll, pitch, yaw]

    def read_altitude(self):
        data = self.unpack_packet(self.request_packet(MSPV2.ALTITUDE), 'ihi')
        if len(data) < 2:
            return None
        altitude = data[0] / 100.0
        velocity = data[1] / 100.0
        baro_altitude = data[2] / 100.0
        return [altitude, velocity, baro_altitude]

    def read_gps_data(self):
        data = self.unpack_packet(self.request_packet(MSPV2.RAW_GPS), '2B2I4H')
        if len(data) < 7:
            return None
        return data

    def set_raw_rc(self, data):
        if len(data) < 16:
            while len(data) < 16:
                data.append(1500)
        self.send_comand(16, self.SET_RAW_RC, data[:16])

    def read_rc(self):
        data = self.unpack_packet(self.request_packet(MSPV2.RC), '16H')
        if len(data) < 16:
            return None
        return data

    def arm(self):
        start_time = time.time()
        while (time.time() - start_time) < 0.5:
            self.set_raw_rc([1500, 1500, 2000, 1000])

    def disarm(self):
        start_time = time.time()
        while (time.time() - start_time) < 0.5:
            self.set_raw_rc([1500, 1500, 1000, 1000])

    def stop(self):
        self.uart.close()


if __name__ == "__main__":
    Uart = serial.Serial(PORT)
    Uart.baudrate = 115200
    Uart.bytesize = serial.EIGHTBITS
    Uart.parity = serial.PARITY_NONE
    Uart.stopbits = serial.STOPBITS_ONE
    Uart.timeout = 0.5
    MSP = MSPV2(Uart)
    a = 0
    while True:
        #if a == 20:
        #    MSP.arm()
        #    print('arm')
        #elif a == 40:
        #    MSP.disarm()
        #    print('disarm')
        #    a = 0
        #if a > 700:
        #    a = 0
        #MSP.set_raw_rc([1500,1500,1500,1000 + a])
        print('========================')
        rc = MSP.read_rc()
        print(rc)
        #a += 1
