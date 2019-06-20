import socket
import struct

FILE_BIN_PATH = "./log/log.bin"
FILE_TEXT_PATH = "./log/log.txt"
IP = "10.10.10.101"
PORT_IN = 1918
PORT_OUT = 1919
MAX_MESSAGE_SIZE = 1024
DATA_FORMAT = "24f"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', PORT_IN))
sock.settimeout(0.01)

log_bin = open(FILE_BIN_PATH, 'wb')
log_text = open(FILE_TEXT_PATH, 'w')

log_text.write('\n')

while True:
    try:
        data, addr = sock.recvfrom(MAX_MESSAGE_SIZE)
    except Exception as e:
        #print(e)
        continue

    log_bin.write(data)
    sock.sendto(data, (IP, PORT_OUT))
    try:
        data_buf = struct.unpack('<' + DATA_FORMAT, data)
        print(data_buf)
        data_str = str(data_buf[0])
        for i in data_buf[1:]:
            data_str = data_str + ',' + str(i)

        data_str = data_str + '\n'

        log_text.write(data_str)
    except Exception as e:
        print(data)

    try:
        data, addr = sock.recvfrom(MAX_MESSAGE_SIZE)
    except Exception as e:
        #print(e)
        continue

    log_bin.write(data)
    sock.sendto(data, (IP, PORT_OUT))
    try:
        data_buf = struct.unpack('<' + DATA_FORMAT, data)
        print(data_buf)
        data_str = str(data_buf[0])
        for i in data_buf[1:]:
            data_str = data_str + ',' + str(i)

        data_str = data_str + '\n'

        log_text.write(data_str)
    except Exception as e:
        print(data)
        print (e)
