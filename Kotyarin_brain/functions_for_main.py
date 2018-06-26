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


def first_data(revolution_log, ads1115, tsl2561):
    voltage = ads1115.read_pins_voltage()

    lux = tsl2561.get_lux()

    pressure = revolution_log.get_data(revolution.DATA_TYPE["pressure"])
    accel = revolution_log.get_data(revolution.DATA_TYPE["accel"])
    gyro = revolution_log.get_data(revolution.DATA_TYPE["gyro"])
    velocity = revolution_log.get_data(revolution.DATA_TYPE["velocity"])
    mag = revolution_log.get_data(revolution.DATA_TYPE["mag"])

    sms_text_list = ["Pressure: " + str(pressure),
                     "Voltage 0: " + str(voltage[0]),
                     "Voltage 1: " + str(voltage[1]),
                     "Voltage 2: " + str(voltage[2]),
                     "Voltage 3: " + str(voltage[3])]
    # -------------------------------------------------------------<==
    # TODO: Make first data list
    # -------------------------------------------------------------<==
    # -------------------------------------------------------------<==
    # TODO: Make sms module
    # -------------------------------------------------------------<==
    return 0


def pressure_now(revolution_log):
    pressure = revolution_log.get_data()
    if ((pressure < PRESSURE_MIN) &
        (pressure > PRESSURE_MAX)):
        return revolution.PRESSURE_NOW
    else:
        raise RevolutionError("Error with pressure value")


def deb_print(str):
    try:
        print str
    except Exception:
        pass
