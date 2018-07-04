import time
import os

from settings import *

PHONE_NUMBER = "+79096709348"

# -------------------------------------------------------------<==
# TODO: Write normal gsm_control_client
# -------------------------------------------------------------<==


class Gsm_control_client():
    def __init__(self, uart=PORT_GSM, pthone_number=PHONE_NUMBER):
        self.phone_number = pthone_number
        self.uart_name = uart
        print "gsm init"

    def setup(self):
        run = open('run_sms.sh', 'w')
        run.write("#!/bin/bash\n")
        run.write("\n")
        string = ("chat -V -f sms_modem.chat > " + self.uart_name +
                  " < " + self.uart_name + "\n")
        run.write(string)

        run.close()

    def sms_send(self, text):
        chat = open('sms_modem.chat', 'w')
        chat.write("ABORT ERROR\n")
        chat.write("ABORT BUSY\n")
        chat.write("TIMEOUT 10\n")
        chat.write("\n")
        chat.write("''  AT\n")
        chat.write("OK  AT+CMGF=1\n")
        chat.write("OK  AT+CNMI=2,1,0,0,0\n")
        string = "OK  AT+CMGS=\"" + self.phone_number + "\"\n"
        chat.write(string)
        for i in text:
            text_str = "\'\'  \"" + i + "\"\n"
            chat.write(text_str)
        text_str = "\'\'  \"Time now:" + str(time.time())
        chat.write(text_str)
        chat.write("\032\"")
        chat.write("\n")
        chat.write("\n")
        chat.write("TIMEOUT 30\n")
        chat.write("OK  \'\'\n")
        chat.close()

        print "SMS------------------------------"
        print self.phone_number
        print "---------------------------------"
        for i in text:
            print str(i)
        print "SMS--end-------------------------"

        # os.system(r'./run_sms.sh')



if __name__ == "__main__":
    gsm = Gsm_control_client("/dev/ttyUSB0")
    gsm.setup()
    gsm.sms_send(["Hi, Curator", "This is test sms",
                  "I want to see how this module will work",
                  "Good luck"])
