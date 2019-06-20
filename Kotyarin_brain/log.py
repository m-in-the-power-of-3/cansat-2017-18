import time

IP = "194.87.103.125"
PORT = 1917

PATH = '/home/pi/kotyarin_brain/telemetry_log/board_telemetry_log_'

LOG_TITLE = ("Time, Voltage 1, Voltage 2, Voltage 3, Pressure, Temperature, Lux, Accel_y, Accel_z, Accel_x,  " +
            "Gyro_x, Gyro_y, Gyro_z, Gps fix , Gps num, Gps lat, Gps lon, Gps height, Gps speed, Gps course, Gps hdop " +
            "Angle 1, Angle 2, Heading\n")

class Log_control_client():
    def __init__(self, path=PATH):
        self.path = path

    def setup(self):
        self.log = open(self.path + time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()) + '.txt', 'w')
        self.log.write(LOG_TITLE)

    def write_data(self, data):
        log_str = ''
        for i in data[:-1]:
            log_str = log_str + str(i) + ','
        log_str = log_str + str(data[-1]) + '\n'
        self.log.write(log_str)

    def stop(self):
        self.log.close()
