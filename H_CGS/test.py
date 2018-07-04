import socket

IP = "10.3.10.203"
PORT = 1917
MESSAGE = "Hello, world"

sock = socket.socket(socket.AF_INET,
                     socket.SOCK_DGRAM)

while True:
	sock.sendto("11,12", (IP, PORT))
