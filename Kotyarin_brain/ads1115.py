# This program can't work with comparator.
from i2cdev import *
import time

DEV_ADDRESS = 0x48
# depends on ADDR sel level:
# GND: 0x48
# VDD: 0x49
# SDA: 0x4A
# SCL: 0x4B

MUX = 0x04
# 0x00: AIN0 - AIN1
# 0x01: AIN0 - AIN3
# 0x02: AIN1 - AIN3
# 0x03: AIN2 - AIN3
# 0x04: AIN0 - GND
# 0x05: AIN1 - GND
# 0x06:	AIN2 - GND
# 0x07:	AIN3 - GND
PGA = 0x00
# 0x00:	+-6,144 B
# 0x01:	+-4,096 B
# 0x02:	+-2,048 B
# 0x03:	+-1,024 B
# 0x04:	+-0,512 B
# 0x05:	+-0,256 B
# 0x06:	+-0,256 B
# 0x07:	+-0,256 B
MODE = 0x01
# 0x00: continuous conversion mode
# 0x01: singl-shot mode
DR = 0x04
# 0x00: 8 Hz
# 0x01: 16 Hz
# 0x02: 32 Hz
# 0x03: 64 Hz
# 0x04: 128 Hz
# 0x05: 250 Hz
# 0x06: 475 Hz
# 0x07: 860 Hz

# Registers:
REG_CONVERSION = 0x00
REG_CONFIG = 0x01
REG_MIN = 0x02
REG_MAX = 0x03

TRY_NUM = 40
ERROR_NUM = 17


class Ads1115_control_client ():
    def __init__(self, i2c_, mux=MUX, pga=PGA,
                 mode=MODE, dr=DR, address=DEV_ADDRESS):
        self.i2c_line = i2c_
        self.i2c_addr = address
        self.config = [REG_CONFIG, 0x00, 0x00]
        self.config[1] = mode | (pga << 1) | (mux << 4)
        self.config[2] = 0x03 | (dr << 5)
        self.k = self._count_k(PGA)
        self.time = self._count_time(dr) * 1.1
        self.telemetry_log_vol = open('telemetry_log/vol.txt', 'a')
        self.telemetry_log_vol.write("Time,vol_0,vol_1,vol_2,vol_3\n")

    def setup(self):
        self.i2c_line.set_addr(self.i2c_addr)
        self.i2c_line.write(self.config)
        if ((self.config[1] & 0x01) != 0x00):
            self.start_conversion()

    def set_mux(self, mux_=MUX):
        self.config[1] = self.config[1]

    def start_conversion(self):
        self.i2c_line.set_addr(self.i2c_addr)

        self.i2c_line.write([self.config[0],
                             self.config[1] | 0x80,
                             self.config[2]])

    def _read_raw_voltage(self):
        self.i2c_line.set_addr(self.i2c_addr)

        self.i2c_line.write([REG_CONVERSION])
        self.raw = self.i2c_line.read(2)

    def read_voltage(self, mux):
        self.config[1] = (self.config[1] & 0x8F) | (mux << 4)
        self.setup()

        time.sleep(self.time)

        tic = 0
        while True:
            self.i2c_line.write([REG_CONFIG])
            state = self.i2c_line.read(2)
            if (state[0] >= 0x80):
                break
            if (tic >= TRY_NUM):
                return ERROR_NUM
            tic += 1

        self._read_raw_voltage()

        raw_ = (self.raw[0] << 8) + self.raw[1]
        if (raw_ >= 32768):
            raw_ = raw_ - 65535
        return raw_ * self.k

    def _count_time(self, dr):
        if (dr == 0x00):
            hz = 8
        elif (dr == 0x01):
            hz = 16
        elif (dr == 0x02):
            hz = 32
        elif (dr == 0x03):
            hz = 64
        elif (dr == 0x04):
            hz = 128
        elif (dr == 0x05):
            hz = 250
        elif (dr == 0x06):
            hz = 475
        elif (dr == 0x07):
            hz = 860
        return 1 / hz

    def _count_k(self, pga):
        if (pga == 0x00):
            voltage_max = 6.144
        elif (pga == 0x01):
            voltage_max = 4.096
        elif (pga == 0x02):
            voltage_max = 2.048
        elif (pga == 0x03):
            voltage_max = 1.024
        elif (pga == 0x04):
            voltage_max = 0.512
        elif (pga >= 0x05):
            voltage_max = 0.256
        return voltage_max / 32768.0

    def read_pins_voltage(self):
        in_0 = self.read_voltage(0x04)
        in_1 = self.read_voltage(0x05)
        in_2 = self.read_voltage(0x06)
        in_3 = self.read_voltage(0x07)

        pins = [in_0, in_1, in_2, in_3]
        self.telemetry_log_vol.write(str(time.time()) + "," +
                                     str(pins[0]) + "," +
                                     str(pins[1]) + "," +
                                     str(pins[2]) + "," +
                                     str(pins[3]) + " \n")

        return pins

    def close(self):
        self.telemetry_log_vol.close()


if __name__ == '__main__':
    i2c_line = I2C(0)
    i2c_line.set_addr(DEV_ADDRESS)
    i2c_line.set_timeout(50)
    ads1115 = Ads1115_control_client(i2c_line)
    ads1115.setup()
    while True:
        in_vol = ads1115.read_pins_voltage()
        out = (str(round(in_vol[0], 2)) + " | " +
               str(round(in_vol[1], 2)) + " | " +
               str(round(in_vol[2], 2)) + " | " +
               str(round(in_vol[3], 2)))
        print out
