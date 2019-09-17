from PyQt5 import QtCore
import sourse.default_config as def_conf
# import config


def init_settings():
    settings = QtCore.QSettings("Agnus", "StrelA")
    settings.Format(QtCore.QSettings.IniFormat)
    settings.Scope(QtCore.QSettings.UserScope)
    return settings


def reset_to_default(settings):
    settings.clear()

    settings.setValue('language', def_conf.LANGUAGE)

    settings.beginGroup("main_window")
    settings.setValue('size', def_conf.MAIN_WINDOW_SIZE)
    settings.setValue('palette', def_conf.MAIN_WINDOW_PALETTE)
    settings.endGroup()

    settings.beginGroup("settings_window")
    settings.setValue('size', def_conf.SETTINGS_WINDOW_SIZE)
    settings.setValue('palette', def_conf.SETTINGS_WINDOW_PALETTE)
    settings.endGroup()

    settings.beginGroup("connection_widget")
    settings.setValue('data_class_name', def_conf.DATA_CLASS_NAME)
    settings.setValue('board_state_is_on', def_conf.BOARD_STATE)
    settings.setValue('packet_size', def_conf.PACKET_SIZE)
    settings.setValue('board_state_num', def_conf.BOARD_STATE_NUM)
    settings.setValue('state_list', def_conf.STATE_LIST)
    settings.setValue('errors_list', def_conf.ERRORS_LIST)
    settings.endGroup()

    settings.beginGroup("log")
    settings.setValue('path', def_conf.LOG_PATH)
    settings.setValue('real_time', def_conf.REAL_TIME)
    settings.setValue('time_delay', def_conf.TIME_DELAY)
    settings.endGroup()

    settings.beginGroup("socket")
    settings.setValue('path', def_conf.SOCKET_LOG_PATH)
    settings.setValue('title', def_conf.SOCKET_LOG_TITLE)
    settings.setValue('port', def_conf.SOCKET_PORT)
    settings.setValue('prefix', def_conf.SOCKET_PREFIX)
    settings.setValue('format', def_conf.DATA_FORMAT)
    settings.endGroup()

    settings.beginGroup("graph_widget")
    settings.setValue('is_on', def_conf.GRAPH_WIDGET)
    settings.setValue('automatic_position', def_conf.GRAPH_WIDGET_AUTOPOSITION)
    settings.beginGroup("graph")
    settings.beginGroup("acceleration")
    settings.setValue('is_on', def_conf.ACCEL_GRAPH)
    settings.setValue('num', def_conf.ACCEL_NUMBER)
    settings.setValue('position', def_conf.ACCEL_POSITION)
    settings.setValue('converter', [def_conf.accel_graph_x_converter,
                                    def_conf.accel_graph_y_converter,
                                    def_conf.accel_graph_z_converter])
    settings.setValue('colour', def_conf.ACCEL_COLOUR)
    settings.endGroup()
    settings.beginGroup("gyro")
    settings.setValue('is_on', def_conf.GYRO_GRAPH)
    settings.setValue('num', def_conf.GYRO_NUMBER)
    settings.setValue('position', def_conf.GYRO_POSITION)
    settings.setValue('converter', [def_conf.gyro_graph_x_converter,
                                    def_conf.gyro_graph_y_converter,
                                    def_conf.gyro_graph_z_converter])
    settings.setValue('colour', def_conf.GYRO_COLOUR)
    settings.endGroup()
    settings.beginGroup("mag")
    settings.setValue('is_on', def_conf.MAG_GRAPH)
    settings.setValue('num', def_conf.MAG_NUMBER)
    settings.setValue('position', def_conf.MAG_POSITION)
    settings.setValue('converter', [def_conf.mag_graph_x_converter,
                                    def_conf.mag_graph_y_converter,
                                    def_conf.mag_graph_z_converter])
    settings.setValue('colour', def_conf.MAG_COLOUR)
    settings.endGroup()
    settings.beginGroup("pressure")
    settings.setValue('is_on', def_conf.PRESSURE_GRAPH)
    settings.setValue('num', def_conf.PRESSURE_NUMBER)
    settings.setValue('position', def_conf.PRESSURE_POSITION)
    settings.setValue('converter', [def_conf.pressure_graph_converter])
    settings.setValue('colour', def_conf.PRESSURE_COLOUR)
    settings.endGroup()
    settings.beginGroup("temperature")
    settings.setValue('is_on', def_conf.TEMPERATURE_GRAPH)
    settings.setValue('num', def_conf.TEMPERATURE_NUMBER)
    settings.setValue('position', def_conf.TEMPERATURE_POSITION)
    settings.setValue('converter', [def_conf.temperature_graph_converter])
    settings.setValue('colour', def_conf.TEMPERATURE_COLOUR)
    settings.endGroup()
    settings.beginGroup("lux")
    settings.setValue('is_on', def_conf.LUX_GRAPH)
    settings.setValue('num', def_conf.LUX_NUMBER)
    settings.setValue('position', def_conf.LUX_POSITION)
    settings.setValue('converter', [def_conf.lux_graph_converter])
    settings.setValue('colour', def_conf.LUX_COLOUR)
    settings.endGroup()
    settings.beginGroup("altitude")
    settings.setValue('is_on', def_conf.ALTITUDE_GRAPH)
    settings.setValue('num', def_conf.ALTITUDE_NUMBER)
    settings.setValue('position', def_conf.ALTITUDE_POSITION)
    settings.setValue('converter', [def_conf.altitude_graph_converter,
                                    def_conf.altitude_baro_graph_converter])
    settings.setValue('colour', def_conf.ALTITUDE_COLOUR)
    settings.endGroup()
    settings.beginGroup("voltage")
    settings.setValue('is_on', def_conf.VOLTAGE_GRAPH)
    settings.setValue('num', def_conf.VOLTAGE_NUMBER)
    settings.setValue('position', def_conf.VOLTAGE_POSITION)
    settings.setValue('converter', [def_conf.voltage_graph_1_converter,
                                    def_conf.voltage_graph_2_converter,
                                    def_conf.voltage_graph_3_converter])
    settings.setValue('colour', def_conf.VOLTAGE_COLOUR)
    settings.endGroup()
    settings.endGroup()
    settings.endGroup()

    settings.beginGroup("map_widget")
    settings.setValue('is_on', def_conf.MAP_WIDGET)
    settings.setValue('center', def_conf.MAP_DEFAULT_CENTER)
    settings.setValue('zoom', def_conf.MAP_DEFAULT_ZOOM)
    settings.setValue('num', def_conf.GPS_NUMBER)
    settings.setValue('converter', def_conf.gps_converter)
    settings.endGroup()

    settings.beginGroup("model_widget")
    settings.setValue('is_on', def_conf.MODEL_WIDGET)
    settings.setValue('num', def_conf.MODEL_NUMBER)
    settings.setValue('converter', [def_conf.model_yaw_converter,
                                    def_conf.model_pitch_converter,
                                    def_conf.model_roll_converter])
    settings.endGroup()



def check_settings(settings):
    if settings.allKeys() == []:
        return False
    else:
        return True
