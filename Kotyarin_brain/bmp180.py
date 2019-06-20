from i2cdev import *

import time


DEV_ADDRESS = 0x77
MODE_ADRESS = 0xF4
ADRESS_TO_READ = 0xF6

# Calibration values
ADRESS_AC1 = 0xAA
ADRESS_AC2 = 0xAC
ADRESS_AC3 = 0xAE
ADRESS_AC4 = 0xB0
ADRESS_AC5 = 0xB2
ADRESS_AC6 = 0xB4
ADRESS_B1 = 0xB6
ADRESS_B2 = 0xB8
ADRESS_MB = 0xBA
ADRESS_MC = 0xBC
ADRESS_MD = 0xBE

# Settings
TEMPERATURE_COD = 0x2E
TIME_TEMPERATURE = 0.005

TIME_PRESSURE = 0.026
PRESSURE_COD = 0xF4

OSS = 0x3
# look at the table
# Temperature | OSS = 00 | CSO = 1 | 01110 | 00101110 = 0x2E | 4,5 mc  | 3 mA | 0,5 C
# Pressure    | OSS = 00 | CSO = 1 | 10100 | 00110100 = 0x34 | 4,5 mc  | 3 mA | 0,6 GPa
# Pressure    | OSS = 01 | CSO = 1 | 10100 | 01110100 = 0x74 | 7,5 mc  | 5 mA | 0,5 GPa
# Pressure    | OSS = 10 | CSO = 1 | 10100 | 10110100 = 0xB4 | 13,5 mc | 7 mA | 0,4 GPa
# Pressure    | OSS = 11 | CSO = 1 | 10100 | 11110100 = 0xF4 | 25,5 mc |12 mA | 0,3 GPa

# Only for test
TEST_AC1 = 408
TEST_AC2 = -72
TEST_AC3 = -14383
TEST_AC4 = 32741
TEST_AC5 = 32757
TEST_AC6 = 23153
TEST_B1 = 6190
TEST_B2 = 4
TEST_MB = -32768
TEST_MC = -8711
TEST_MD = 2868


class Bmp180_control_client ():
    def __init__(self, i2c, dev_addr=DEV_ADDRESS, temp_cod=TEMPERATURE_COD,
                 temp_time=TIME_TEMPERATURE, press_cod=PRESSURE_COD,
                 press_time=TIME_PRESSURE, oss_=OSS):
        self.oss = oss_
        self.pressure_cod = press_cod
        self.pressure_time = press_time
        self.temperature_cod = temp_cod
        self.temperature_time = temp_time
        self.i2c_line = i2c
        self.i2c_addr = dev_addr
        self.calibration_values = {}
        self.pressure = 0
        self.temperature = 0

    def setup(self):
        self.i2c_line.set_addr(self.i2c_addr)

        self._read_calibration_values()

    def _read_calibration_value(self, value_adress, value_name, signed):
        self.i2c_line.write([value_adress])
        value = self.i2c_line.read(2)
        self.calibration_values[value_name] = (value[0] << 8) + value[1]
        if (self.calibration_values[value_name] > 32767) and signed:
            self.calibration_values[value_name] -= 65536

    def _read_calibration_values(self):
        self.i2c_line.set_addr(self.i2c_addr)
        # AC1
        self._read_calibration_value(ADRESS_AC1, "AC1", True)
        # AC2
        self._read_calibration_value(ADRESS_AC2, "AC2", True)
        # AC3
        self._read_calibration_value(ADRESS_AC3, "AC3", True)
        # AC4
        self._read_calibration_value(ADRESS_AC4, "AC4", False)
        # AC5
        self._read_calibration_value(ADRESS_AC5, "AC5", False)
        # AC6
        self._read_calibration_value(ADRESS_AC6, "AC6", False)
        # B1
        self._read_calibration_value(ADRESS_B1, "B1", True)
        # B2
        self._read_calibration_value(ADRESS_B2, "B2", True)
        # MB
        self._read_calibration_value(ADRESS_MB, "MB", True)
        # MC
        self._read_calibration_value(ADRESS_MC, "MC", True)
        # MD
        self._read_calibration_value(ADRESS_MD, "MD", True)

    def read_raw_pressure(self):
        self.i2c_line.write([MODE_ADRESS, self.pressure_cod])
        time.sleep(self.pressure_time)
        self.i2c_line.write([ADRESS_TO_READ])
        value = self.i2c_line.read(3)
        raw_pressure = (value[0] << 16) + (value[1] << 8) + value[2]
        raw_pressure = raw_pressure >> (8 - self.oss)
        return raw_pressure

    def read_raw_temperature(self):
        self.i2c_line.write([MODE_ADRESS, self.temperature_cod])
        time.sleep(self.temperature_time)
        self.i2c_line.write([ADRESS_TO_READ])
        value = self.i2c_line.read(2)
        raw_temperature = (value[0] << 8) + value[1]
        return raw_temperature

    def count_B5(self, raw_temperature):
        X1 = ((raw_temperature - self.calibration_values["AC6"]) * self.calibration_values["AC5"]) >> 15
        X2 = (self.calibration_values["MC"] << 11) // (X1 + self.calibration_values["MD"])
        return X1 + X2

    def count_pressure(self, B5, raw_pressure):
        B6 = B5 - 4000

        X1 = (self.calibration_values["B2"] * ((B6 * B6) >> 12)) >> 11
        X2 = (self.calibration_values["AC2"] * B6) >> 11
        X3 = X1 + X2

        B3 = (((self.calibration_values["AC1"] * 4 + X3) << self.oss) + 2) // 4
        X1 = (self.calibration_values["AC3"] * B6) >> 13
        X2 = (self.calibration_values["B1"] * ((B6 * B6) >> 12)) >> 16
        X3 = ((X1 + X2) + 2) >> 2

        B4 = (self.calibration_values["AC4"] * (X3 + 32768)) >> 15
        B7 = (raw_pressure - B3) * (50000 >> self.oss)

        if (B7 < 0x80000000):
            P = (B7 * 2) // B4
        else:
            P = (B7 // B4) * 2

        X1 = (P >> 8) * (P >> 8)
        X1 = (X1 * 3038) >> 16
        X2 = (-7357 * P) >> 16
        self.pressure = P + ((X1 + X2 + 3791) >> 4)

    def count_temperature(self, B5):
        self.temperature = (B5 + 8) >> 4

    def update_data(self):
        self.i2c_line.set_addr(self.i2c_addr)
        raw_pressure = self.read_raw_pressure()
        raw_temperature = self.read_raw_temperature()

        B5 = self.count_B5(raw_temperature)
        self.count_pressure(B5, raw_pressure)
        self.count_temperature(B5)

    def get_pressure(self):
        return self.pressure

    def get_temperature(self):
        return self.temperature


if __name__ == "__main__":
    i2c_line = I2C(0)
    i2c_line.set_addr(DEV_ADDRESS)
    i2c_line.set_timeout(10)
    bmp180 = Bmp180_control_client(i2c_line)
    bmp180.setup()
    while True:
        bmp180.update_data()
        press = bmp180.get_pressure()
        temp = bmp180.get_temperature()
        print ('pressure:')
        print (press)
        print ('temperature:')
        print (temp)
        time.sleep(0.1)
