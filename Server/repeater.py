import socket
import struct
import time
from smsc_api import *

FILE_BIN_PATH = "./log/log_"
FILE_TEXT_PATH = "./log/log_"
IP = "10.10.10.101"
PORT_IN = 1918
PORT_OUT = 1919
MAX_MESSAGE_SIZE = 1024
DATA_FORMAT = "28f"
STATE_NUM = 27

LOG_TITLE = ("Time, Voltage 1, Voltage 2, Voltage 3, Pressure, Temperature, Lux, Accel_x, Accel_y, Accel_z,  " +
             "Mag_x, Mag_y, Mag_z, Gyro_x, Gyro_y, Gyro_z, Gps fix , Gps num, Gps lat, Gps lon, Gps height, Gps speed, " +
             "Gps course, Gps hdop, Angle 1, Angle 2, Heading, State\n")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', PORT_IN))
sock.settimeout(0.01)

log_bin = open(FILE_BIN_PATH + time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()) + '.bin', 'wb')
log_text = open(FILE_TEXT_PATH + time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()) + '.txt', 'w')

log_text.write(LOG_TITLE)

while True:
    try:
        data, addr = sock.recvfrom(MAX_MESSAGE_SIZE)
    except Exception as e:
        print(e)
        continue

    log_bin.write(data)
    sock.sendto(data, (IP, PORT_OUT))
    try:
        data_buf = struct.unpack('<' + DATA_FORMAT, data)
    except Exception as e:
        print(data)
    else:
        print(data_buf)
        data_str = str(data_buf[0])
        for i in data_buf[1:]:
            data_str = data_str + ',' + str(i)
        data_str = data_str + '\n'
        log_text.write(data_str)