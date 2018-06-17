# This program works only for type = 0x00 and integration time = 402 ms.
from i2cdev import *
import time


DEV_ADDRESS = 0x39
# depends on ADDR sel level:
# GND - 0x29
# Float - 0x39
# VDD - 0x49
T_INT = 2
I_GAIN = 0x10
# 0x00: x1
# 0x10: x16
I_TYPE = 0x00
# 0x00: T, FN, CL type
# 0x01: CS type

# Registers:
REG_CONTROL = 0x00
REG_TIMING = 0x01
REG_THRESH_LOW_LOW = 0x02
REG_THRESH_LOW_HIGH = 0x03
REG_THRESH_HIGH_LOW = 0x04
REG_THRESH_HIGH_HIGH = 0x05
REG_INTERRUPT = 0x06
REG_CRC = 0x08
REG_ID = 0x0A
REG_DATA_0_LOW = 0x0C
REG_DATA_0_HIGH = 0x0D
REG_DATA_1_LOW = 0x0E
REG_DATA_1_HIGH = 0x0F

CMD_TEMPLATE = 0x80

RATIO_SCALE = 9
LUX_SCALE = 14
CH_SCALE = 10
CHSCALE_TINT0 = 0x7517
CHSCALE_TINT1 = 0x0fe7

# Only for i_type = 0x00
K1C = 0x0043
B1C = 0x0204
M1C = 0x01ad
K2C = 0x0085
B2C = 0x0228
M2C = 0x02c1
K3C = 0x00c8
B3C = 0x0253
M3C = 0x0363
K4C = 0x010a
B4C = 0x0282
M4C = 0x03df
K5C = 0x014d
B5C = 0x0177
M5C = 0x01dd
K6C = 0x019a
B6C = 0x0101
M6C = 0x0127
K7C = 0x029a
B7C = 0x0037
M7C = 0x002b
K8C = 0x029a
B8C = 0x0000
M8C = 0x0000
K1T = 0x0040
B1T = 0x01f2
M1T = 0x01be
K2T = 0x0080
B2T = 0x0214
M2T = 0x02d1
K3T = 0x00c0
B3T = 0x023f
M3T = 0x037b
K4T = 0x0100
B4T = 0x0270
M4T = 0x03fe
K5T = 0x0138
B5T = 0x016f
M5T = 0x01fc
K6T = 0x019a
B6T = 0x00d2
M6T = 0x00fb
K7T = 0x029a
B7T = 0x0018
M7T = 0x0012
K8T = 0x029a
B8T = 0x0000
M8T = 0x0000


class Tsl2561_control_client ():
    def __init__(self, i2c_, i_type=I_TYPE,
                 i_gain=I_GAIN, address=DEV_ADDRESS):
        self.gain = i_gain
        self.ch_scale = (1 << CH_SCALE)

        if (not self.gain):
            self.ch_scale = self.ch_scale << 4

        self.type = i_type
        self.addr = address
        self.i2c_line = i2c_
        self.i2c_addr = address
        self.data_1 = -1
        self.data_0 = -1

    def setup(self):
        self.i2c_line.set_addr(self.i2c_addr)

        self.telemetry_log_lux = open('telemetry_log/lux.txt', 'a')
        self.telemetry_log_lux.write("Time,LUX\n")

        self._write_reg(REG_CONTROL, 0x03)
        self._write_reg(REG_TIMING, 0x02 | self.gain)
        self._write_reg(REG_INTERRUPT, 0x00)

    def _write_reg(self, reg, val):
        data = [CMD_TEMPLATE | reg]
        data.append(val)
        i2c_line.write(data)

    def _read_raw_lux(self):
        self.i2c_line.set_addr(self.i2c_addr)

        self.i2c_line.write([0x80 | 0x20 | 0x0E])
        buf = self.i2c_line.read(2)
        self.data_1 = (buf[1] << 8) | buf[0]

        self.i2c_line.write([0x80 | 0x20 | 0x0C])
        buf = self.i2c_line.read(2)
        self.data_0 = (buf[1] << 8) | buf[0]

    def get_lux(self):
        self._read_raw_lux()

        channel_0 = (self.data_0 * self.ch_scale) >> CH_SCALE
        channel_1 = (self.data_1 * self.ch_scale) >> CH_SCALE

        ratio1 = 0
        if (channel_0 != 0):
            ratio1 = (channel_1 << (RATIO_SCALE + 1)) / channel_0

        ratio = (ratio1 + 1) >> 1

        if (self.type == 0x00):
            if ((ratio >= 0) and (ratio <= K1T)):
                b = B1T
                m = M1T
            elif (ratio <= K2T):
                b = B2T
                m = M2T
            elif (ratio <= K3T):
                b = B3T
                m = M3T
            elif (ratio <= K4T):
                b = B4T
                m = M4T
            elif (ratio <= K5T):
                b = B5T
                m = M5T
            elif (ratio <= K6T):
                b = B6T
                m = M6T
            elif (ratio <= K7T):
                b = B7T
                m = M7T
            elif (ratio > K8T):
                b = B8T
                m = M8T

        elif (self.type == 0x01):
            if ((ratio >= 0) and (ratio <= K1C)):
                b = B1C
                m = M1C
            elif (ratio <= K2C):
                b = B2C
                m = M2C
            elif (ratio <= K3C):
                b = B3C
                m = M3C
            elif (ratio <= K4C):
                b = B4C
                m = M4C
            elif (ratio <= K5C):
                b = B5C
                m = M5C
            elif (ratio <= K6C):
                b = B6C
                m = M6C
            elif (ratio <= K7C):
                b = B7C
                m = M7C
            elif (ratio > K8C):
                b = B8C
                m = M8C

        temp = (channel_0 * b) - (channel_1 * m)

        if (temp < 0):
            temp = 0

        temp += (1 << (LUX_SCALE - 1))
        lux = temp >> LUX_SCALE
        self.telemetry_log_lux.write(str(time.time()) + "," +
                                     str(lux) + " \n")
        return lux

    def close(self):
        self.telemetry_log_lux.close()


if __name__ == '__main__':
    i2c_line = I2C(0)
    i2c_line.set_addr(DEV_ADDRESS)
    i2c_line.set_timeout(50)
    tsl2561 = Tsl2561_control_client(i2c_line)
    tsl2561.setup()
    while True:
        lux = tsl2561.get_lux()
        print lux
        time.sleep(0.5)
