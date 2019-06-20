import sourse.settings.palette as palette
#!/usr/bin/python3
LANGUAGE = 'en'
COLOUR_THEME = 'dark'
# ==============================================================================
# Data
# ==============================================================================
TOTAL_DATA_NUM = 13
# ------------------------------------------------------------------------------
# Log
# ------------------------------------------------------------------------------
LOG_PATH = './log/telemetry_log/telemetry_log_int.txt'
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
# Central widget
# ==============================================================================
CONNECTION_WIDGET_PALETTE = palette.dark

# ==============================================================================
# Graph widget
# ==============================================================================
GRAPH_WIDGET = True

ACCEL_GRAPH = True
ACCEL_NUMBER = [2, 4, 3]
ACCEL_CONVERTER = lambda value: value
ACCEL_POSITION = [0, 0]
ACCEL_COLOUR = ['r', 'g', 'b']

GYRO_GRAPH = False
GYRO_NUMBER = [5, 6, 7]
GYRO_CONVERTER = lambda value: value
GYRO_POSITION = [0, 1]
GYRO_COLOUR = ['r', 'g', 'b']

TEMPERATURE_GRAPH = True
TEMPERATURE_NUMBER = 6
TEMPERATURE_CONVERTER = lambda value: value
TEMPERATURE_POSITION = [1, 0]
TEMPERATURE_COLOUR = 'r'

PRESSURE_GRAPH = True
PRESSURE_NUMBER = 5
PRESSURE_CONVERTER = lambda value: value
PRESSURE_POSITION = [2, 0]
PRESSURE_COLOUR = 'r'

MAG_GRAPH = False
MAG_NUMBER = 1
MAG_CONVERTER = lambda value: value
MAG_POSITION = [2, 1]
MAG_COLOUR = 'r'

VOLTAGE_GRAPH = False
VOLTAGE_NUMBER = [2, 3, 4]
VOLTAGE_CONVERTER = lambda value: value
VOLTAGE_POSITION = [1, 1]
VOLTAGE_COLOUR = ['r', 'g', 'b']

# ==============================================================================
# Map widget
# ==============================================================================
MAP_WIDGET = True
MAP_DEFAULT_CENTER = [56.43488, 37.429475]
MAP_DEFAULT_ZOOM = 13
# lat, lon, height
GPS_NUMBER = [11, 10, 12]
GPS_CONVERTER = lambda value: value / 100

# ==============================================================================
# Command line widget
# ==============================================================================
COMMAND_LINE_WIDGET = True

# ==============================================================================
# Model widget
# ==============================================================================
MODEL_WIDGET = True

# ==============================================================================
# Connection widget
# ==============================================================================
BOARD_STATE = True
BOARD_STATE_NUMBER = 1
STATE_LIST = ['Before start', 'In the rocket', 'Free fall', 'Flight to the point', 'Payload dumping', 'Return to home']
ERRORS_LIST = ['Low battery']


