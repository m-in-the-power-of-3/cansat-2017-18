import serial
import time

import i2cdev

import revolution
import ads1115
import tsl2561
import fuse
import gsm
import trigger
import buzzer
import bmp180

from settings import *
from errors import *

# Global
uart_revolution = 0
uart_gsm = 0
i2c_line = 0
uav_talk = 0
revolution_log = 0
revolution_servo = 0
pi_bmp180 = 0
pi_tsl2561 = 0
pi_ads1115 = 0
pi_fuse = 0
pi_buzzer = 0
pi_gsm = 0
pi_trigger = 0

# Data
pressure_at_start = 0
data_lux = -1
lux_max = -1
lux_min = 65537
voltage_list = [0]


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


# BMP180
def init_bmp180():
    global pi_bmp180
    global i2c_line

    try:
        pi_bmp180 = bmp180.Bmp180_control_client(i2c_line)
        pi_bmp180.setup()
    except Exception:
        raise BMP180Error("Init BMP180 error")

# GSM
def init_gsm():
    global pi_gsm
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

    init_bmp180()
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


# BMP180
def deinit_bmp180():
    global pi_bmp180

    if not (pi_bmp180 == 0):
        pi_bmp180.close()

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

    deinit_bmp180()


# ================================================================
# Data
# ================================================================
# Pressure
def get_pressure():
    try:
        global revolution_log
        global pi_bmp180

        #if (not (revolution_log == 0)):
        #    pressure = revolution_log.get_data("press")
        #    if ((pressure > PRESSURE_MIN) and
        #        (pressure < PRESSURE_MAX)):
        #        return pressure
        #    else:
        #        raise ValueError()
# <<------------------------------------------------------------------Rewritten. Use BMP180
        if (not (pi_bmp180 == 0)):
            pressure = pi_bmp180.get_pressure()
            if ((pressure > PRESSURE_MIN) and
                (pressure < PRESSURE_MAX)):
                return pressure
            else:
                raise ValueError()
    except Exception():
        #raise RevolutionError("Error with pressure value")
        raise BMP180Error("Error with pressure value")


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


def check_lux():
    global data_lux
    global lux_min
    global lux_max

    if not ((data_lux == -1) or (lux_min == 65537) or (lux_max == -1)):
        level = LUX_LEVEL_K * (lux_max - lux_min)
        level = level + lux_min
        if (data_lux > level):
            return True
    return False


def count_min_lux():
    global data_lux
    global lux_min
    global lux_max

    if ((not (data_lux == -1)) and (data_lux < lux_min)):
        lux_min = data_lux


def count_max_lux():
    global data_lux
    global lux_max

    if ((not (data_lux == -1)) and (data_lux > lux_max)):
        lux_max = data_lux


def check_voltage(voltage):
    if (voltage.len() == 4):
        voltage_1 = voltage[0]
        voltage_2 = (voltage[1] * K23) - voltage_1
        voltage_3 = (voltage[2] * K34) - (voltage[1] * K23)
        voltage_4 = (voltage[3] * K4) - (voltage[2] * K34)

        if ((voltage_1 < VOLTAGE_MIN) or
            (voltage_2 < VOLTAGE_MIN) or
            (voltage_3 < VOLTAGE_MIN) or
            (voltage_4 < VOLTAGE_MIN)):

            raise BatteryError()


def check_data():
    global data_lux

    if (not (pi_tsl2561 == 0)):
        try:
            data_lux = get_lux()
        except TSL2561Error:
            data_lux = -1

    if (not (pi_bmp180 == 0)):
        try:
            pi_bmp180.update_data()
        except Exception:
            raise BMP180Error("Update data from BMP180 error")

    if (not (pi_ads1115 == 0)):
        try:
            voltage_list == get_voltage()
        except ADS1115Error:
            deb_print("Ads1115 value error")
        else:
            try:
                print "voltage off"
                # check_voltage(voltage_list)
            except BatteryError:
                raise


def buzzer_control(mode):
    if mode:
        pi_buzzer.on()
    else:
        pi_buzzer.off()


def check_height(height_action):
    global pressure_at_start

    try:
        pressure = get_pressure()
        x = pressure / pressure_at_start
        height = 44330 * (1.0 - pow(x, 0.1903))
    except:
        pass
    height = input()
    if (height_action >= height):
        return True
    else:
        return False


def save_pressure_at_start():
    global pressure_at_start

    pressure_at_start = get_pressure()

def open_parachute():
    global pi_fuse

    pi_fuse.start()
    time.sleep(FUSE_TIMEOUT)
    pi_fuse.stop()

# ================================================================
# Debug
# ================================================================


def deb_print(str):
    try:
        print str
    except Exception:
        pass
