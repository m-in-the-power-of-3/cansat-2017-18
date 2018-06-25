import serial

import i2cdev

import revolution
import ads1115
import tsl2561
import fuse

from settings import *
from errors import *


def init_all():
    # NPNA
    # ------------------------------------------------------------
    # Uart
    uart_revolution = serial.Serial(PORT_REVOLUTION,
                                    BAUDRATE_REVOLUTION,
                                    timeout=TIMEOUT_REVOLUTION)

    if not uart_revolution.isOpen():
        raise IOError("Uart for revolution open error")

    uart_gsm = serial.Serial(PORT_GSM,
                             BAUDRATE_GSM,
                             timeout=TIMEOUT_GSM)

    if not uart_gsm.isOpen():
        raise IOError("Uart for gsm open error")

    # I2C
    try:
        i2c_line = i2cdev.I2C(PORT_I2C)
        i2c_line.set_timeout(I2C_TIMEOUT)
    except Exception:
        raise IOError("I2c open error")

    # Revolution
    # -------------------------------------------------------------
    try:
        # UAV talk
        uav_talk = revolution.Uavtalk()
        uav_talk.setup(uart_revolution)
    except Exception:
        raise UAVTalkError("Start Uav talk error")

    try:
        # Revolution - log
        revolution_log = revolution.All_telemetry_logger(uav_talk,
                                                         REV_LOG_UPDATE_RATE)
        revolution_log.setup_all()

        # Revolution - servo
        revolution_servo = revolution.Servo_control_client(uav_talk,
                                                           REV_SERVO_CHANNEL,
                                                           REV_SERVO_MIN,
                                                           REV_SERVO_MAX,
                                                           REV_SERVO_DEG,)
    except Exception:
        raise RevolutionError("Init servo and log error")

    # Device
    # ------------------------------------------------------------
    # Buzzer
    # -------------------------------------------------------------<==
    # TODO: write module for buzzer
    # -------------------------------------------------------------<==

    # GSM
    # -------------------------------------------------------------<==
    # TODO: write module for GSM
    # -------------------------------------------------------------<==

    # TSL2561
    try:
        pi_tsl2561 = tsl2561.Tsl2561_control_client()
        pi_tsl2561.setup()
    except Exception:
        raise TSL2561Error("Init tsl2561 error")

    # ADS1115
    try:
        pi_ads1115 = ads1115.Ads1115_control_client(i2c_line)
        ads1115.setup()
    except Exception:
        raise ADS1115Error("Init ADS1115 error")

    return {"log": revolution_log,
            "servo": revolution_servo,
            "tsl2561": pi_tsl2561,
            "ads1115": pi_ads1115}

    # Fuse
    try:
        pi_fuse = fuse.fuse_control_client()
        pi_fuse.setup()
    except Exception:
        raise FuseError("Init Fuse error")


def deb_print(str):
    try:
        print str
    except Exception:
        pass
