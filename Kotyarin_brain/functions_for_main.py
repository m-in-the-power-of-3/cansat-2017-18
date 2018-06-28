import serial

import i2cdev

import revolution
import ads1115
import tsl2561
import fuse
import gsm
import trigger
import buzzer

from settings import *
from errors import *

# Global
uart_revolution = 0
uart_gsm = 0
i2c_line = 0
uav_talk = 0
revolution_log = 0
revolution_servo = 0
pi_tsl2561 = 0
pi_ads1115 = 0
pi_fuse = 0
pi_buzzer = 0
pi_gsm = 0
pi_trigger = 0


# ================================================================
# Init
# ================================================================
# ----------------------------------------------------------------
# NPNA
# ----------------------------------------------------------------
# Uart
def init_uart():
    global uart_revolution
    global uart_gsm

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
def init_i2c():
    global i2c_line

    try:
        i2c_line = i2cdev.I2C(0)
        i2c_line.set_timeout(I2C_TIMEOUT)
    except Exception:
        raise IOError("I2c open error")


# ----------------------------------------------------------------
# Revolution
# ----------------------------------------------------------------
def init_revolution():
    global uav_talk
    global revolution_log
    global revolution_servo

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


# ----------------------------------------------------------------
# Device
# ----------------------------------------------------------------
# Buzzer
def init_buzzer():
    global pi_buzzer

    try:
        pi_buzzer = buzzer.Buzzer_control_client()
        pi_buzzer.setup()
    except Exception:
        raise BuzzerError("Init Buzzer error")


# -------------------------------------------------------------<==
# TODO: write module for GSM
# -------------------------------------------------------------<==
# GSM
def init_gsm():
    global pi_gsm
    # Added only for test
    pi_gsm = gsm.Gsm_control_client()


# TSL2561
def init_tsl1561():
    global pi_tsl2561
    global i2c_line

    try:
        pi_tsl2561 = tsl2561.Tsl2561_control_client(i2c_line)
        pi_tsl2561.setup()
    except Exception:
        raise TSL2561Error("Init tsl2561 error")


# ADS1115
def init_ads1115():
    global pi_ads1115
    global i2c_line

    try:
        pi_ads1115 = ads1115.Ads1115_control_client(i2c_line)
        pi_ads1115.setup()
    except Exception:
        raise ADS1115Error("Init ADS1115 error")


# Fuse
def init_fuse():
    global pi_fuse

    try:
        pi_fuse = fuse.Fuse_control_client()
        pi_fuse.setup()
    except Exception:
        raise FuseError("Init Fuse error")


# Trigger
def init_trigger():
    global pi_trigger

    try:
        pi_trigger = trigger.Trigger_control_client()
        pi_trigger.setup()
    except Exception:
        raise TriggerError("Init trigger error")


# ----------------------------------------------------------------
# Init all
# ----------------------------------------------------------------
def init_all():
    init_uart()
    init_i2c()
    init_trigger()
    init_fuse()

    init_gsm()
    init_buzzer()

    # init_revolution()

    init_tsl1561()
    init_ads1115()




# ================================================================
# Deinit
# ================================================================
# ----------------------------------------------------------------
# Revolution
# ----------------------------------------------------------------
def deinit_revolution():
    global uav_talk
    global revolution_log

    if not (uav_talk == 0):
        uav_talk.stop()
    if not (revolution_log == 0):
        revolution_log.close()


# ----------------------------------------------------------------
# Device
# ----------------------------------------------------------------
# Buzzer
def deinit_buzzer():
    global pi_buzzer

    if not (pi_buzzer == 0):
        pi_buzzer.stop()


# -------------------------------------------------------------<==
# TODO: write module for GSM
# -------------------------------------------------------------<==
# GSM
def deinit_gsm():
    print "gsm deinit"


# TSL2561
def deinit_tsl1561():
    global pi_tsl2561

    if not (pi_tsl2561 == 0):
        pi_tsl2561.close()


# ADS1115
def deinit_ads1115():
    global pi_ads1115

    if not (pi_ads1115 == 0):
        pi_ads1115.close()


# ----------------------------------------------------------------
# Init all
# ----------------------------------------------------------------
def deinit_all():
    deinit_gsm()
    deinit_buzzer()

    deinit_revolution()

    deinit_tsl1561()
    deinit_ads1115()


# ================================================================
# Data
# ================================================================
# Pressure
def get_pressure():
    try:
        global revolution_log
        pressure = revolution_log.get_data("press")
        if ((pressure > PRESSURE_MIN) &
            (pressure < PRESSURE_MAX)):
            return pressure
        else:
            raise ValueError()
    except Exception():
        raise RevolutionError("Error with pressure value")


# Voltage
def get_voltage():
    try:
        global pi_ads1115
        voltage = pi_ads1115.read_pins_voltage()
        return voltage
    except Exception():
        raise ADS1115Error("Error with voltage value")


# Lux
def get_lux():
    try:
        global pi_tsl2561
        lux = pi_tsl2561.get_lux()
        return lux
    except Exception():
        raise TSL2561Error("Error with lux value")


# Accel
def get_accel():
    try:
        global revolution_log
        accel = revolution_log.get_data(revolution.DATA_TYPE["accel"])
        return accel
    except Exception():
        raise RevolutionError("Error with accel value")


# ================================================================
# Link
# ================================================================
def sms(text):
    try:
        global pi_gsm
        pi_gsm.sms_send(text)
    except Exception:
        raise GsmError("Send SMS error")


# ================================================================
# Action
# ================================================================
def check_trigger():
    global pi_trigger

    try:
        trig = pi_trigger.read()

        if (trig == 1):
            return True
        elif (trig == 0):
            return False
        else:
            raise ValueError()
    except Exception:
        raise TriggerError("Trigger Error")


def buzzer_control(mode):
    if mode:
        pi_buzzer.on()
    else:
        pi_buzzer.off()
# ================================================================
# Debug
# ================================================================


def deb_print(str):
    try:
        print str
    except Exception:
        pass
