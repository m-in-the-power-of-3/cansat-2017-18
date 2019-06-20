import socket
import struct

IP = "127.0.0.1"
PORT_IN = 1917
PORT_OUT = 1918
MAX_MESSAGE_SIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', PORT_IN))
sock.settimeout(0.01)
num = 2
byte = 0
data_concut = b'0'


while True:
    try:
        data, addr = sock.recvfrom(MAX_MESSAGE_SIZE)
    except Exception as e:
        continue

    byte = data[0]
    #print(len(data[1:]))


    if byte == num:
        data_concut = data_concut + data[1:]
        num = num + 1
        continue
    print(len(data_concut))
    sock.sendto(data_concut, (IP, PORT_OUT))

    if byte == 1:
        data_concut = data[1:]
        num = 2
        continue
