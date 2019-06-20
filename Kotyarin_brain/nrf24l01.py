from RF24 import *

PIPES = [0xDDDDDDDDDD, 0xF4F4F4F4F4]
CHANNEL = 47
ADDRESS_WIDTH = 5
DATA_RATE = RF24_1MBPS
CRC_LEN = RF24_CRC_16
CE_PIN = 6
NRF24_FREQ = 500000

class Nrf24l01_control_client ():
    def __init__(self, freq=NRF24_FREQ, ce_pin=CE_PIN,
                 channel=CHANNEL, addr_wight=ADDRESS_WIDTH,
                 data_rate=DATA_RATE, crc_len=CRC_LEN, pipes=PIPES):
        self.freq = freq
        self.ce_pin = ce_pin
        self.channel = channel
        self.addr_wight = addr_wight
        self.data_rate = data_rate
        self.crc_len = crc_len
        self.pipes = pipes

    def setup(self):
        self.radio = RF24(self.ce_pin, 0, self.freq)
        self.radio.begin()
        self.radio.setChannel(self.channel)
        self.radio.setAddressWidth(self.addr_wight)
        self.radio.setDataRate(self.data_rate)
        self.radio.setCRCLength(self.crc_len)
        self.radio.enableDynamicPayloads()
        self.radio.openWritingPipe(self.pipes[1])

    def show_settings(self):
        self.radio.printDetails()

    def send_data(self, data):
        self.radio.write(data, 1)
 