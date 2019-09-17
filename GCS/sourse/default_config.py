#!/usr/bin/python3
from sourse.data_class import log_data
from sourse.data_class import socket_data

LANGUAGE = 'en'

# ------------------------------------------------------------------------------
# Log
# ------------------------------------------------------------------------------
LOG_PATH = '/home/developer/git/cansat-2017-2018/GCS/log/log_2019_07_05_09_25_14.txt'
REAL_TIME = 1
TIME_DELAY = 0.1

# ------------------------------------------------------------------------------
# Socket
# ------------------------------------------------------------------------------
SOCKET_PORT = 1918
DATA_FORMAT = "28f"
SOCKET_LOG_TITLE = ("Time, Voltage 1, Voltage 2, Voltage 3, Pressure, Temperature, Lux, Accel_x, Accel_y, Accel_z,  " +
                    "Mag_x, Mag_y, Mag_z, Gyro_x, Gyro_y, Gyro_z, Gps fix , Gps num, Gps lat, Gps lon, Gps height, Gps speed, " +
                    "Gps course, Gps hdop, Angle 1, Angle 2, Heading, State\n")
SOCKET_LOG_PATH = "/home/developer/git/cansat-2017-2018/GCS/log/telemetry_log/"
SOCKET_PREFIX = "telemetry_log_"

# ==============================================================================
# Main window
# ==============================================================================
MAIN_WINDOW_SIZE = [1024, 768]
MAIN_WINDOW_PALETTE = 'dark'

# ==============================================================================
# Connection widget
# ==============================================================================
DATA_CLASS_NAME = 'log'
BOARD_STATE = 1
PACKET_SIZE = 33
BOARD_STATE_NUM = 27
STATE_LIST = ['Init', 'First data', 'Before start', 'Wait 100',
              'in the rocket', 'separate wait', 'prepare for flight',
              'lending', 'wp', 'drop', 'rth']
ERRORS_LIST = ['Filesafe']

# ==============================================================================
# Settings window
# ==============================================================================
SETTINGS_WINDOW_SIZE = [512, 384]
SETTINGS_WINDOW_PALETTE = 'dark'

# ==============================================================================
# Graph widget
# ==============================================================================
GRAPH_WIDGET = 1
GRAPH_WIDGET_AUTOPOSITION = 1

ACCEL_GRAPH = 0
ACCEL_NUMBER = [7, 8, 9]
ACCEL_POSITION = [0, 0]
ACCEL_COLOUR = 'rgb'


def accel_graph_x_converter(value):
    return value


def accel_graph_y_converter(value):
    return value


def accel_graph_z_converter(value):
    return value

GYRO_GRAPH = 0
GYRO_NUMBER = [10, 11, 12]
GYRO_POSITION = [0, 1]
GYRO_COLOUR = 'rgb'


def gyro_graph_x_converter(value):
    return value


def gyro_graph_y_converter(value):
    return value


def gyro_graph_z_converter(value):
    return value

MAG_GRAPH = 0
MAG_NUMBER = [13, 14, 15]
MAG_POSITION = [0, 1]
MAG_COLOUR = 'rgb'


def mag_graph_x_converter(value):
    return value


def mag_graph_y_converter(value):
    return value


def mag_graph_z_converter(value):
    return value

VOLTAGE_GRAPH = 0
VOLTAGE_NUMBER = [28, 29, 30]
VOLTAGE_POSITION = [0, 1]
VOLTAGE_COLOUR = 'rgb'

voltage_1 = 0
voltage_2 = 0


def voltage_graph_1_converter(value):
    return value


def voltage_graph_2_converter(value):
    return value


def voltage_graph_3_converter(value):
    return value

TEMPERATURE_GRAPH = 0
TEMPERATURE_NUMBER = [5]
TEMPERATURE_POSITION = [1, 0]
TEMPERATURE_COLOUR = 'r'


def temperature_graph_converter(value):
    return value / 10.0

PRESSURE_GRAPH = 0
PRESSURE_NUMBER = [31]
PRESSURE_POSITION = [2, 0]
PRESSURE_COLOUR = 'r'


def pressure_graph_converter(value):
    return value

LUX_GRAPH = 0
LUX_NUMBER = [6]
LUX_POSITION = [2, 0]
LUX_COLOUR = 'r'


def lux_graph_converter(value):
    return value

ALTITUDE_GRAPH = 1
ALTITUDE_NUMBER = [32]
ALTITUDE_POSITION = [2, 0]
ALTITUDE_COLOUR = 'b'


def altitude_graph_converter(value):
    return value


def altitude_baro_graph_converter(value):
    return value
# ==============================================================================
# Map widget
# ==============================================================================
MAP_WIDGET = 1
MAP_DEFAULT_CENTER = [56.40771840, 40.98595520]
MAP_DEFAULT_ZOOM = 17
# lat, lon, height
GPS_NUMBER = [18, 19, 20]


def gps_converter(value):
    return value / 10000000

# ==============================================================================
# Model widget
# ==============================================================================
MODEL_WIDGET = 1
MODEL_NUMBER = [24, 25, 26]


def model_yaw_converter(value):
    return value


def model_pitch_converter(value):
    return value


def model_roll_converter(value):
    return value