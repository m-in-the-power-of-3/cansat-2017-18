from PyQt5 import QtCore, QtWidgets, QtGui
import config
import sourse.settings.default_config as default_config


def set_converters():
    converters = {}
    try:
        converters.update({"accel_graph": config.ACCEL_CONVERTER})
    except Exception:
        converters.update({"accel_graph": default_config.ACCEL_CONVERTER})
    try:
        converters.update({"gyro_graph": config.GYRO_CONVERTER})
    except Exception:
        converters.update({"gyro_graph": default_config.GYRO_CONVERTER})
    try:
        converters.update({"pressure_graph": config.PRESSURE_CONVERTER})
    except Exception:
        converters.update({"pressure_graph": default_config.PRESSURE_CONVERTER})
    try:
        converters.update({"temperature_graph": config.TEMPERATURE_CONVERTER})
    except Exception:
        converters.update({"temperature_graph": default_config.TEMPERATURE_CONVERTER})
    try:
        converters.update({"mag_graph": config.MAG_CONVERTER})
    except Exception:
        converters.update({"mag_graph": default_config.MAG_CONVERTER})
    try:
        converters.update({"voltage_graph": config.VOLTAGE_CONVERTER})
    except Exception:
        converters.update({"voltage_graph": default_config.VOLTAGE_CONVERTER})
    return converters


def update_settings(settings):
    print('settings')
    settings.clear()

    settings.beginGroup("main_window")
    settings.setValue('size', config.MAIN_WINDOW_SIZE)
    settings.setValue('palette', config.MAIN_WINDOW_PALETTE)
    settings.endGroup()

    settings.beginGroup("settings_window")
    settings.setValue('size', config.SETTINGS_WINDOW_SIZE)
    settings.setValue('palette', config.SETTINGS_WINDOW_PALETTE)
    settings.endGroup()

    settings.beginGroup("central_widget")
    settings.setValue('palette', config.CENTRAL_WIDGET_PALETTE)
    settings.endGroup()

    settings.beginGroup("graph_widget")

    settings.setValue('is_on', config.GRAPH_WIDGET)
    settings.beginGroup("accel_graph")
    settings.setValue('is_on', 1)
    settings.setValue('num', config.ACCEL_NUMBER)
    settings.setValue('position', config.ACCEL_POSITION)
    settings.setValue('colour', config.ACCEL_COLOUR)
    settings.endGroup()
    settings.beginGroup("gyro_graph")
    settings.setValue('is_on', config.GYRO_GRAPH)
    settings.setValue('num', config.GYRO_NUMBER)
    settings.setValue('position', config.GYRO_POSITION)
    settings.setValue('colour', config.GYRO_COLOUR)
    settings.endGroup()
    settings.beginGroup("pressure_graph")
    settings.setValue('is_on', config.PRESSURE_GRAPH)
    settings.setValue('num', config.PRESSURE_NUMBER)
    settings.setValue('position', config.PRESSURE_POSITION)
    settings.setValue('colour', config.PRESSURE_COLOUR)
    settings.endGroup()
    settings.beginGroup("temperature_graph")
    settings.setValue('is_on', config.TEMPERATURE_GRAPH)
    settings.setValue('num', config.TEMPERATURE_NUMBER)
    settings.setValue('position', config.TEMPERATURE_POSITION)
    settings.setValue('colour', config.TEMPERATURE_COLOUR)
    settings.endGroup()
    settings.beginGroup("mag_graph")
    settings.setValue('is_on', config.MAG_GRAPH)
    settings.setValue('num', config.MAG_NUMBER)
    settings.setValue('position', config.MAG_POSITION)
    settings.setValue('colour', config.MAG_COLOUR)
    settings.endGroup()
    settings.beginGroup("voltage_graph")
    settings.setValue('is_on', config.VOLTAGE_GRAPH)
    settings.setValue('num', config.VOLTAGE_NUMBER)
    settings.setValue('position', config.VOLTAGE_POSITION)
    settings.setValue('colour', config.VOLTAGE_COLOUR)
    settings.endGroup()

    settings.endGroup()

    settings.beginGroup("model_widget")
    settings.setValue('is_on', config.MODEL_WIDGET)
    settings.endGroup()

    settings.beginGroup("map_widget")
    settings.setValue('is_on', config.MAP_WIDGET)
    settings.endGroup()

    settings.beginGroup("connection_widget")
    settings.setValue('palette', config.CONNECTION_WIDGET_PALETTE)
    settings.setValue('data_class', config.DATA_CLASS)
    settings.endGroup()

    settings.beginGroup("command_line_widget")
    settings.setValue('is_on', config.COMMAND_LINE_WIDGET)
    settings.endGroup()

def update_settings_default(settings):
    pass