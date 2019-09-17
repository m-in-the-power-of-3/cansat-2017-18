#!/usr/bin/python3
import socket
import struct
import time

PORT = 1918

DATA_FORMAT = "28f" #'5fhH9h2B2I4H3hB'
LOG_TITLE = ("Time, Voltage 1, Voltage 2, Voltage 3, Pressure, Temperature, Lux, Accel_y, Accel_z, Accel_x,  " +
            "Gyro_x, Gyro_y, Gyro_z, Gps fix , Gps num, Gps lat, Gps lon, Gps height, Gps speed, Gps course, Gps hdop " +
            "Angle 1, Angle 2, Heading\n")
LOG_PATH = "/home/developer/git/cansat-2017-2018/GCS/log/telemetry_log/telemetry_log_"

class Data_source():
    def __init__(self, port=PORT, data_format=DATA_FORMAT, log_path=LOG_PATH, log_title=LOG_TITLE):
        self.port = port
        print(port)
        self.data_format = data_format
        self.log_path = log_path
        self.log_title = log_title
        self.last_message_time = 0

    def start(self):
        self.log = open(self.log_path + time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()) + '.txt', 'w')
        self.log.write(self.log_title)
        self.sock = socket.socket(socket.AF_INET,
                                  socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', self.port))
        self.sock.settimeout(1)

    def change_log_path(self, log_path):
        self.log_path = log_path

    def read_data(self):
        return_data = []
        data, addr = self.sock.recvfrom(1024)
        return_data = list(struct.unpack('<' + self.data_format, data))

        if self.last_message_time >= return_data[0]:
            raise ValueError

        self.last_message_time = return_data[0]

        log_str = ''
        for i in return_data[:-1]:
            log_str = log_str + str(i) + ','
        log_str = log_str + str(return_data[-1]) + '\n'
        self.log.write(log_str)

        return return_data

    def stop(self):
        self.log.close()

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Only for test
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

if __name__ == '__main__':
    print("start")
    obJ = Data_source()
    print("start")
    obJ.start()
    while True:
        try:
            data = obJ.read_data()
            print (data)
        except Exception as e:
            print(e)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
