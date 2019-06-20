from bmp180 import *
from i2cdev import *
from math import sqrt
import time

if __name__ == '__main__':
    i2c_line = I2C(0)
    bmp180 = Bmp180_control_client(i2c_line)
    bmp180.setup()

    pressure_at_start = 0
    temperature_at_start = 0
    for i in range(1, 6):
        bmp180.update_data()
        pressure = bmp180.get_pressure()
        temperature = bmp180.get_temperature() / 10.0
        print(str(i) + ' pressure = ' + str(pressure))
        print(str(i) + ' temperature = ' + str(temperature))
        pressure_at_start += pressure
        temperature_at_start += temperature
        time.sleep(1)
    pressure_at_start = pressure_at_start / 5.0
    temperature_at_start = temperature_at_start / 5.0
    print ('Start pressure = ' + str(pressure_at_start))
    print ('Start temperature = ' + str(temperature_at_start))
    p = (0.029 * pressure_at_start) / (8.314459848 * (temperature_at_start + 273))
    print ('Start p = ' + str(p))
    print ('======= Begin =======')
    time_start = time.time()
    pressure_max = 0
    while True:
        time_now = time.time()
        if (time_now - time_start) < 2.0:
            bmp180.update_data()
            pressure = bmp180.get_pressure()
            if pressure_max < pressure:
                pressure_max = pressure
        else:
            pressure = pressure_max
            x = (2 * (pressure - pressure_at_start) / p)
            if x > 0:
                speed = sqrt(x) * 1.015
                print(pressure)
            else:
                speed = -1
                print (pressure)
            print (speed)
            pressure_max = 0
            time_start = time.time()
