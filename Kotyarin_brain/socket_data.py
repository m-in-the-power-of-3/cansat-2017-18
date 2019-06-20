import socket

IP = "194.87.103.125"
PORT = 1917


class Socket_control_client():
    def __init__(self, ip=IP, port=PORT):
        self.port = port
        self.ip = ip

    def setup(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(1)

    def send_data(self, data):
        self.socket.sendto(data, (self.ip, self.port))
