#!/usr/bin/python3
import sourse.settings.palette as palette
from sourse.data_class import log_data
from sourse.data_class import socket_data

LANGUAGE = 'en'
COLOUR_THEME = 'dark'
# ------------------------------------------------------------------------------
# Log
# ------------------------------------------------------------------------------
LOG_PATH = '/home/developer/git/cansat-2017-2018/GCS/log/telemetry_log/board_telemetry_log_2019_05_19_12_49_31.txt'
REAL_TIME = False
TIME_DELAY = 0.01

# ==============================================================================
# Main window
# ==============================================================================
MAIN_WINDOW_SIZE = [1024, 768]
MAIN_WINDOW_PALETTE = palette.dark

# ==============================================================================
# Settings window
# ==============================================================================
SETTINGS_WINDOW_SIZE = [512, 384]
SETTINGS_WINDOW_PALETTE = palette.dark

# ==============================================================================
# Central widget
# ==============================================================================
CENTRAL_WIDGET_PALETTE = palette.dark

# ==============================================================================
# Connection widget
# ==============================================================================
CONNECTION_WIDGET_PALETTE = palette.dark
DATA_CLASS = socket_data.Data_source(LOG_PATH)

# ==============================================================================
# Graph widget
# ==============================================================================
GRAPH_WIDGET = True

ACCEL_GRAPH = True
ACCEL_NUMBER = [7, 8, 9]
ACCEL_CONVERTER = lambda value: value
ACCEL_POSITION = [0, 0]
ACCEL_COLOUR = 'rgb'

GYRO_GRAPH = True
GYRO_NUMBER = [10, 11, 12]
GYRO_CONVERTER = lambda value: value
GYRO_POSITION = [0, 1]
GYRO_COLOUR = 'rgb'

TEMPERATURE_GRAPH = True
TEMPERATURE_NUMBER = [5]
TEMPERATURE_CONVERTER = lambda value: value / 10.0
TEMPERATURE_POSITION = [1, 0]
TEMPERATURE_COLOUR = 'r'

PRESSURE_GRAPH = True
PRESSURE_NUMBER = [4]
PRESSURE_CONVERTER = lambda value: value
PRESSURE_POSITION = [2, 0]
PRESSURE_COLOUR = 'r'

MAG_GRAPH = True
MAG_NUMBER = [13, 14, 15]
MAG_CONVERTER = lambda value: value
MAG_POSITION = [2, 1]
MAG_COLOUR = 'rgb'

VOLTAGE_GRAPH = True
VOLTAGE_NUMBER = [6]
VOLTAGE_CONVERTER = lambda value: value
VOLTAGE_POSITION = [1, 1]
VOLTAGE_COLOUR = 'rgb'

#ADD lux graph

# ==============================================================================
# Map widget
# ==============================================================================
MAP_WIDGET = True
MAP_DEFAULT_CENTER = [56.43488, 37.429475]
MAP_DEFAULT_ZOOM = 13
# lat, lon, height
GPS_NUMBER = [18, 19, 20]
GPS_CONVERTER = lambda value: value / 10000000

# ==============================================================================
# Command line widget
# ==============================================================================
COMMAND_LINE_WIDGET = True

# ==============================================================================
# Model widget
# ==============================================================================
MODEL_WIDGET = True
MODEL_NUMBER = [24, 25, 26]

# ==============================================================================
# Connection widget
# ==============================================================================
BOARD_STATE = True
BOARD_STATE_NUMBER = 1
STATE_LIST = ['Before start', 'In the rocket', 'Free fall', 'Flight to the point', 'Payload dumping', 'Return to home']
ERRORS_LIST = ['Low battery']


