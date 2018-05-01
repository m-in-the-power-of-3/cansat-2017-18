import logging
import serial
import traceback
import sys

from librepilot.uavtalk.uavobject import *
from librepilot.uavtalk.uavtalk import *
from librepilot.uavtalk.objectManager import *
from librepilot.uavtalk.connectionManager import *

import revolution



if __name__ == '__main__':

    if len(sys.argv) != 2:
        print "ERROR: Incorrect number of arguments"
        sys.exit(2)

    port = sys.argv[1]

    UavT = revolution.Uavtalk()
    UavT.setup(port)

    Telemetry_log = revolution.All_telemetry_logger(UavT,50)
    Telemetry_log.setup_all()

    Servo = revolution.Servo_control_client(UavT,0,1000,2000,180)

    while True:
        try:
            a = int(input())
        except:
            a = -1
        if (a >= 0):
            print "Rotation"
            Servo.rotation(a)
