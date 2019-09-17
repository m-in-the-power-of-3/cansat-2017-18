from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPalette
import gettext
import time

import pyqtgraph as PG
import pyqtgraph.opengl as OpenGL
import numpy as NumPy
from stl import mesh as StlMesh
from itertools import chain
from math import acos, trunc


from sourse.map_sourse.PyQtMap import Open_street_map
import sourse.settings_control as settings_ctrl
import sourse.palette as palette
from sourse.language.language import *
import user_settings
import sourse.data_class.socket_data as socket_data
import sourse.data_class.log_data as log_data

import satellite_model

ICON_PATH = "./strela_icon.png"
MAIN_PROPERTIES_ICON_PATH = "./strela_icon.png"
CONNECTION_PROPERTIES_ICON_PATH = "./strela_icon.png"
MAP_PROPERTIES_ICON_PATH = "./strela_icon.png"
MODEL_PROPERTIES_ICON_PATH = "./strela_icon.png"
GRAPH_PROPERTIES_ICON_PATH = "./strela_icon.png"
ARROW_ICON_PATH = "./strela_icon.png"
GREY_ARROW_ICON_PATH = "./strela_icon.png"

ICON_PATH_PASSIVE = "http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_gray.png"
ICON_PATH_ACTIVE = "http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_red.png"

MESH_PATH = './satellite_model_new.stl'

#_ = lambda x: x

class Abstract_properties(QtWidgets.QWidget):
    def __init__(self):
        super(Abstract_properties, self).__init__()
        self.settings = settings_ctrl.init_settings()

    def exeption_action(self, e):
        if self.status_bar is not None:
            self.status_bar.showMessage(str(e))
        print(e)
        time.sleep(0.1)

    def read_int_from_edit_list(self, edit_list):
        num_list = []
        for edit in edit_list:
            num = self.read_int_from_edit(edit)
            if num is None:
                return None
            num_list.append(num)
        return num_list

    def read_int_from_edit(self, edit):
        try:
            num = int(edit.text())
        except Exception as e:
            self.exeption_action(e)
            return None
        return num

    def read_float_from_edit_list(self, edit_list):
        num_list = []
        for edit in edit_list:
            num = self.read_float_from_edit(edit)
            if num is None:
                return None
            num_list.append(num)
        return num_list

    def read_float_from_edit(self, edit):
        try:
            num = float(edit.text())
        except Exception as e:
            self.exeption_action(e)
            return None
        return num

    def read_obj_from_combo_box(self, combo_box, obj_list):
        try:
            obj = obj_list[combo_box.currentIndex()]
        except Exception as e:
            self.exeption_action(e)
            return None
        return obj

    def check_state_to_bool(self, state):
        if state == 0:
            return 0
        else:
            return 1

    def num_bool_to_check_state(self, num_boolean):
        if int(num_boolean):
            return 2
        else:
            return 0

    def update_setting(self, function, sourse, setting_addr):
        setting = function(sourse)
        if setting is not None:
            self.settings.setValue(setting_addr, setting)

    def update_setting_arg(self, function, sourse, arg, setting_addr):
        setting = function(sourse, arg)
        if setting is not None:
            self.settings.setValue(setting_addr, setting)


class Main_properties_widget(Abstract_properties):
    def __init__(self, status_bar=None):
        super(Main_properties_widget, self).__init__()
        self.status_bar = status_bar

        self.setup_ui()
        self.setup_ui_settings()

    def setup_ui_settings(self):
        self.window_size_label.setText(_('Window size'))
        self.window_palette_label.setText(_('Window palette'))
        self.settings_window_size_label.setText(_('Settings window size'))
        self.settings_window_palette_label.setText(_('Settings window size'))
        self.language_label.setText(_('Languege'))

    def setup_ui(self):
        self.layout = QtWidgets.QGridLayout(self)

        self.window_size_label = QtWidgets.QLabel()
        self.window_size_edit = [QtWidgets.QLineEdit(str(self.settings.value('main_window/size')[0])),
                                 QtWidgets.QLineEdit(str(self.settings.value('main_window/size')[1]))]
        self.layout.addWidget(self.window_size_label, self.layout.rowCount(), 0)
        for i in range(len(self.window_size_edit)):
            self.layout.addWidget(self.window_size_edit[i], self.layout.rowCount() - 1, i + 1)

        self.window_palette_label = QtWidgets.QLabel()
        self.window_palette_combo_box = QtWidgets.QComboBox()
        self.window_palette_combo_box.addItems(palette.palette_list.keys())
        self.window_palette_combo_box.setCurrentText(self.settings.value('main_window/palette'))
        self.layout.addWidget(self.window_palette_label, self.layout.rowCount(), 0)
        self.layout.addWidget(self.window_palette_combo_box, self.layout.rowCount() - 1, 1)

        self.settings_window_size_label = QtWidgets.QLabel()
        self.settings_window_size_edit = [QtWidgets.QLineEdit(str(self.settings.value('settings_window/size')[0])),
                                          QtWidgets.QLineEdit(str(self.settings.value('settings_window/size')[1]))]
        self.layout.addWidget(self.settings_window_size_label, self.layout.rowCount(), 0)
        for i in range(len(self.settings_window_size_edit)):
            self.layout.addWidget(self.settings_window_size_edit[i], self.layout.rowCount() - 1, i + 1)

        self.settings_window_palette_label = QtWidgets.QLabel()
        self.settings_window_palette_combo_box = QtWidgets.QComboBox()
        self.settings_window_palette_combo_box.addItems(palette.palette_list.keys())
        self.settings_window_palette_combo_box.setCurrentText(self.settings.value('settings_window/palette'))
        self.layout.addWidget(self.settings_window_palette_label, self.layout.rowCount(), 0)
        self.layout.addWidget(self.settings_window_palette_combo_box, self.layout.rowCount() - 1, 1)

        self.language_label = QtWidgets.QLabel()
        self.language_combo_box = QtWidgets.QComboBox()
        self.language_combo_box.addItems(language_list)
        self.language_combo_box.setCurrentIndex(language_list.index(self.settings.value('language')))
        self.layout.addWidget(self.language_label, self.layout.rowCount(), 0)
        self.layout.addWidget(self.language_combo_box, self.layout.rowCount() - 1, 1)

    def update_settings(self):
        self.update_setting(self.read_int_from_edit_list, self.window_size_edit, 'main_window/size')
        self.settings.setValue('main_window/palette', self.window_palette_combo_box.currentText())
        self.update_setting(self.read_int_from_edit_list, self.settings_window_size_edit, 'settings_window/size')
        self.settings.setValue('settings_window/palette', self.settings_window_palette_combo_box.currentText())
        self.update_setting_arg(self.read_obj_from_combo_box, self.language_combo_box, language_list, 'language')


class Model_properties_widget(Abstract_properties):
    def __init__(self, change_settings, status_bar=None):
        super(Model_properties_widget, self).__init__()
        self.status_bar = status_bar

        self.setup_ui()
        self.setup_ui_settings()

    def setup_ui_settings(self):
        self.is_on_check_box.setText(_('Enable Model'))
        self.num_label.setText(_('Angle number (x, y, z)'))

    def setup_ui(self):
        self.layout = QtWidgets.QGridLayout(self)

        self.is_on_check_box = QtWidgets.QCheckBox()
        self.is_on_check_box.setTristate(False)
        self.is_on_check_box.setCheckState(self.num_bool_to_check_state(self.settings.value('model_widget/is_on')))
        self.layout.addWidget(self.is_on_check_box, self.layout.rowCount(), 0, 1, 3)

        self.num_label = QtWidgets.QLabel()
        self.num_edit = [QtWidgets.QLineEdit(str(self.settings.value('model_widget/num')[0])),
                         QtWidgets.QLineEdit(str(self.settings.value('model_widget/num')[1])),
                         QtWidgets.QLineEdit(str(self.settings.value('model_widget/num')[2]))]
        self.layout.addWidget(self.num_label, self.layout.rowCount(), 0)
        for i in range(len(self.num_edit)):
            self.layout.addWidget(self.num_edit[i], self.layout.rowCount() - 1, i + 1)

    def update_settings(self):
        self.settings.setValue('model_widget/is_on', self.check_state_to_bool(self.is_on_check_box.checkState()))
        self.update_setting(self.read_int_from_edit_list, self.num_edit, 'model_widget/num')
        try:
            self.settings.setValue('model_widget/converter', [user_settings.model_yaw_converter,
                                                              user_settings.model_pitch_converter,
                                                              user_settings.model_roll_converter])
        except Exception as e:
            self.exeption_action(e)


class Map_properties_widget(Abstract_properties):
    def __init__(self, change_settings, status_bar=None):
        super(Map_properties_widget, self).__init__()
        self.status_bar = status_bar

        self.setup_ui()
        self.setup_ui_settings()

    def setup_ui_settings(self):
        self.is_on_check_box.setText(_('Enable Map'))
        self.center_label.setText(_('Map center'))
        self.zoom_label.setText(_('Map zoom'))
        self.num_label.setText(_('Map number (lat, lon, height)'))

    def setup_ui(self):
        self.layout = QtWidgets.QGridLayout(self)

        self.is_on_check_box = QtWidgets.QCheckBox()
        self.is_on_check_box.setTristate(False)
        self.is_on_check_box.setCheckState(self.num_bool_to_check_state(self.settings.value('map_widget/is_on')))
        self.layout.addWidget(self.is_on_check_box, self.layout.rowCount(), 0, 1, 3)

        self.center_label = QtWidgets.QLabel()
        self.center_edit = [QtWidgets.QLineEdit(str(self.settings.value('map_widget/center')[0])),
                            QtWidgets.QLineEdit(str(self.settings.value('map_widget/center')[1]))]
        self.layout.addWidget(self.center_label, self.layout.rowCount(), 0)
        self.layout.addWidget(self.center_edit[0], self.layout.rowCount() - 1, 1)
        self.layout.addWidget(self.center_edit[1], self.layout.rowCount() - 1, 2, 1, 2)

        self.zoom_label = QtWidgets.QLabel()
        self.zoom_edit = QtWidgets.QLineEdit(str(self.settings.value('map_widget/zoom')))
        self.layout.addWidget(self.zoom_label, self.layout.rowCount(), 0)
        self.layout.addWidget(self.zoom_edit, self.layout.rowCount() - 1, 1, 1, 3)

        self.num_label = QtWidgets.QLabel()
        self.num_edit = [QtWidgets.QLineEdit(str(self.settings.value('map_widget/num')[0])),
                         QtWidgets.QLineEdit(str(self.settings.value('map_widget/num')[1])),
                         QtWidgets.QLineEdit(str(self.settings.value('map_widget/num')[2]))]
        self.layout.addWidget(self.num_label, self.layout.rowCount(), 0)
        for i in range(len(self.num_edit)):
            self.layout.addWidget(self.num_edit[i], self.layout.rowCount() - 1, i + 1)

    def update_settings(self):
        self.settings.setValue('map_widget/is_on', self.check_state_to_bool(self.is_on_check_box.checkState()))
        self.update_setting(self.read_float_from_edit_list, self.center_edit, 'map_widget/center')
        self.update_setting(self.read_int_from_edit, self.zoom_edit, 'map_widget/zoom')
        self.update_setting(self.read_int_from_edit_list, self.num_edit, 'map_widget/num')
        try:
            self.settings.setValue('map_widget/converter', user_settings.gps_converter)
        except Exception as e:
            self.exeption_action(e)


class Log_properties_widget(Abstract_properties):
    def __init__(self, status_bar=None):
        super(Log_properties_widget, self).__init__()
        self.status_bar = status_bar

        self.setAutoFillBackground(True)

        self.setup_ui()
        self.setup_ui_settings()

    def setup_ui_settings(self):
        self.btn_path.setText(_("Set log path"))
        self.real_time_check_box.setText(_('Real time'))
        self.time_delay_label.setText(_('Time delay'))

    def setup_ui(self):
        self.layout = QtWidgets.QGridLayout(self)

        self.path = self.settings.value('log/path')
        self.path_label = QtWidgets.QLabel(self.path[self.path.rfind('/') + 1:])
        self.btn_path = QtWidgets.QPushButton()
        self.btn_path.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.btn_path.clicked.connect(self.show_dialog)
        self.layout.addWidget(self.path_label, self.layout.rowCount(), 0)
        self.layout.addWidget(self.btn_path, self.layout.rowCount() - 1, 1)

        self.real_time_check_box = QtWidgets.QCheckBox()
        self.real_time_check_box.setTristate(False)
        self.real_time_check_box.setCheckState(self.num_bool_to_check_state(self.settings.value('log/real_time')))
        self.layout.addWidget(self.real_time_check_box, self.layout.rowCount(), 0, 1, 2)

        self.time_delay_label = QtWidgets.QLabel()
        self.time_delay_edit = QtWidgets.QLineEdit(str(self.settings.value('log/time_delay')))
        self.layout.addWidget(self.time_delay_label, self.layout.rowCount(), 0)
        self.layout.addWidget(self.time_delay_edit, self.layout.rowCount() - 1, 1)

    def update_settings(self):
        self.settings.setValue('log/path', self.path)
        self.settings.setValue('log/real_time', self.check_state_to_bool(self.real_time_check_box.checkState()))
        self.update_setting(self.read_float_from_edit, self.time_delay_edit, 'log/time_delay')

    def show_dialog(self):
        self.path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './log/telemetry_log/')[0]
        self.path_label.setText(self.path[self.path.rfind('/') + 1:])


class Plot_properties_widget(Abstract_properties):
    def __init__(self, graph, status_bar=None):
        super(Plot_properties_widget, self).__init__()
        self.status_bar = status_bar
        self.graph = graph

        self.setAutoFillBackground(True)

        self.setup_ui()
        self.setup_ui_settings()

    def setup_ui_settings(self):
        self.num_label.setText(_('Data num'))
        self.position_label.setText(_('Position'))
        self.colour_label.setText(_('Colour (r, g, b)'))

    def setup_ui(self):
        self.layout = QtWidgets.QGridLayout(self)

        self.settings.beginGroup('graph_widget')
        self.settings.beginGroup('graph')
        self.settings.beginGroup(self.graph)
        self.num_label = QtWidgets.QLabel()
        self.num_edit = []
        for num in self.settings.value('num'):
            self.num_edit.append(QtWidgets.QLineEdit(str(num)))
        self.layout.addWidget(self.num_label, self.layout.rowCount(), 0)
        for i in range(len(self.num_edit)):
            self.layout.addWidget(self.num_edit[i], self.layout.rowCount() - 1, i + 1)

        self.position_label = QtWidgets.QLabel()
        self.position_edit = [QtWidgets.QLineEdit(str(self.settings.value('position')[0])),
                              QtWidgets.QLineEdit(str(self.settings.value('position')[1]))]
        self.layout.addWidget(self.position_label, self.layout.rowCount(), 0)
        for i in range(len(self.position_edit)):
            self.layout.addWidget(self.position_edit[i], self.layout.rowCount() - 1, i + 1)

        self.colour_label = QtWidgets.QLabel()
        self.colour_edit = QtWidgets.QLineEdit(str(self.settings.value('colour')))
        self.layout.addWidget(self.colour_label, self.layout.rowCount(), 0)
        self.layout.addWidget(self.colour_edit, self.layout.rowCount() - 1, 1)
        self.settings.endGroup()
        self.settings.endGroup()
        self.settings.endGroup()

    def update_settings(self):
        self.settings.beginGroup('graph_widget')
        self.settings.beginGroup('graph')
        self.settings.beginGroup(self.graph)
        self.update_setting(self.read_int_from_edit_list, self.num_edit, 'num')
        self.update_setting(self.read_int_from_edit_list, self.position_edit, 'position')
        self.settings.setValue('colour', self.colour_edit.text())
        self.settings.endGroup()
        self.settings.endGroup()
        self.settings.endGroup()


class Graph_properties_widget(Abstract_properties):
    def __init__(self, change_settings, status_bar=None):
        super(Graph_properties_widget, self).__init__()
        self.status_bar = status_bar

        self.setup_ui()
        self.setup_ui_settings()

    def setup_ui_settings(self):
        self.graph_check_box.setText(_('Graph'))
        self.acceleration_check_box.setText(_('Acceleration'))
        self.gyro_check_box.setText(_('Gyro'))
        self.mag_check_box.setText(_('Mag'))
        self.pressure_check_box.setText(_('Pressure'))
        self.temperature_check_box.setText(_('Temperature'))
        self.lux_check_box.setText(_('Lux'))
        self.altitude_check_box.setText(_('Altitude'))
        self.voltage_check_box.setText(_('Voltage'))
        self.plot_label.setText(_('Plot settings'))
        self.automatic_position_check_box.setText(_('Automatic_position'))

    def setup_ui(self):
        self.layout = QtWidgets.QGridLayout(self)

        self.graph_check_box = QtWidgets.QCheckBox()
        self.graph_check_box.setTristate(False)
        self.graph_check_box.setCheckState(self.num_bool_to_check_state(self.settings.value('graph_widget/is_on')))
        self.layout.addWidget(self.graph_check_box, self.layout.rowCount(), 0)

        self.acceleration_check_box = QtWidgets.QCheckBox()
        self.acceleration_check_box.setTristate(False)
        self.acceleration_check_box.setCheckState(self.num_bool_to_check_state(self.settings.value('graph_widget/graph/acceleration/is_on')))
        self.layout.addWidget(self.acceleration_check_box, self.layout.rowCount(), 0)

        self.gyro_check_box = QtWidgets.QCheckBox()
        self.gyro_check_box.setTristate(False)
        self.gyro_check_box.setCheckState(self.num_bool_to_check_state(self.settings.value('graph_widget/graph/gyro/is_on')))
        self.layout.addWidget(self.gyro_check_box, self.layout.rowCount(), 0)

        self.mag_check_box = QtWidgets.QCheckBox()
        self.mag_check_box.setTristate(False)
        self.mag_check_box.setCheckState(self.num_bool_to_check_state(self.settings.value('graph_widget/graph/mag/is_on')))
        self.layout.addWidget(self.mag_check_box, self.layout.rowCount(), 0)

        self.pressure_check_box = QtWidgets.QCheckBox()
        self.pressure_check_box.setTristate(False)
        self.pressure_check_box.setCheckState(self.num_bool_to_check_state(self.settings.value('graph_widget/graph/pressure/is_on')))
        self.layout.addWidget(self.pressure_check_box, self.layout.rowCount(), 0)

        self.temperature_check_box = QtWidgets.QCheckBox()
        self.temperature_check_box.setTristate(False)
        self.temperature_check_box.setCheckState(self.num_bool_to_check_state(self.settings.value('graph_widget/graph/temperature/is_on')))
        self.layout.addWidget(self.temperature_check_box, self.layout.rowCount(), 0)

        self.lux_check_box = QtWidgets.QCheckBox()
        self.lux_check_box.setTristate(False)
        self.lux_check_box.setCheckState(self.num_bool_to_check_state(self.settings.value('graph_widget/graph/lux/is_on')))
        self.layout.addWidget(self.lux_check_box, self.layout.rowCount(), 0)

        self.altitude_check_box = QtWidgets.QCheckBox()
        self.altitude_check_box.setTristate(False)
        self.altitude_check_box.setCheckState(self.num_bool_to_check_state(self.settings.value('graph_widget/graph/altitude/is_on')))
        self.layout.addWidget(self.altitude_check_box, self.layout.rowCount(), 0)

        self.voltage_check_box = QtWidgets.QCheckBox()
        self.voltage_check_box.setTristate(False)
        self.voltage_check_box.setCheckState(self.num_bool_to_check_state(self.settings.value('graph_widget/graph/voltage/is_on')))
        self.layout.addWidget(self.voltage_check_box, self.layout.rowCount(), 0)

        self.plot_label = QtWidgets.QLabel()
        self.plot_combo_box = QtWidgets.QComboBox()
        self.plot_combo_box.addItems(['acceleration', 'gyro', 'mag', 'pressure', 'temperature', 'lux', 'altitude', 'voltage'])
        self.plot_combo_box.activated.connect(self.change_plot_properties)
        self.layout.addWidget(self.plot_label, self.layout.rowCount(), 0)
        self.layout.addWidget(self.plot_combo_box, self.layout.rowCount() - 1, 1)
        self.property_row = self.layout.rowCount()
        self.set_plot_properties()

        self.automatic_position_check_box = QtWidgets.QCheckBox()
        self.automatic_position_check_box.setTristate(False)
        self.automatic_position_check_box.setCheckState(self.num_bool_to_check_state(self.settings.value('graph_widget/automatic_position')))
        self.layout.addWidget(self.automatic_position_check_box, self.layout.rowCount(), 0)

    def update_settings(self):
        self.settings.setValue('graph_widget/graph/acceleration/is_on', self.check_state_to_bool(self.acceleration_check_box.checkState()))
        self.settings.setValue('graph_widget/graph/gyro/is_on', self.check_state_to_bool(self.gyro_check_box.checkState()))
        self.settings.setValue('graph_widget/graph/mag/is_on', self.check_state_to_bool(self.mag_check_box.checkState()))
        self.settings.setValue('graph_widget/graph/pressure/is_on', self.check_state_to_bool(self.pressure_check_box.checkState()))
        self.settings.setValue('graph_widget/graph/temperature/is_on', self.check_state_to_bool(self.temperature_check_box.checkState()))
        self.settings.setValue('graph_widget/graph/lux/is_on', self.check_state_to_bool(self.lux_check_box.checkState()))
        self.settings.setValue('graph_widget/graph/altitude/is_on', self.check_state_to_bool(self.altitude_check_box.checkState()))
        self.settings.setValue('graph_widget/graph/voltage/is_on', self.check_state_to_bool(self.voltage_check_box.checkState()))
        self.property.update_settings()
        self.settings.setValue('graph_widget/automatic_position', self.check_state_to_bool(self.automatic_position_check_box.checkState()))

    def set_plot_properties(self):
        self.property = self.property = Plot_properties_widget(self.plot_combo_box.currentText(), self.status_bar)
        self.layout.addWidget(self.property, self.property_row, 0, 1, 2)

    def change_plot_properties(self):
        self.layout.removeWidget(self.property)
        self.set_plot_properties()


class Socket_properties_widget(Abstract_properties):
    def __init__(self, status_bar=None):
        super(Socket_properties_widget, self).__init__()
        self.status_bar = status_bar

        self.setAutoFillBackground(True)

        self.setup_ui()
        self.setup_ui_settings()

    def setup_ui_settings(self):
        self.port_label.setText(_("Port"))
        self.format_label.setText(_("Format"))
        self.btn_path.setText(_('Log directory'))
        self.log_prefix_label.setText(_('Log prefix'))
        self.log_title_label.setText(_('Log title'))

    def setup_ui(self):
        self.layout = QtWidgets.QGridLayout(self)

        self.port_label = QtWidgets.QLabel()
        self.port_edit = QtWidgets.QLineEdit(str(self.settings.value('socket/port')))
        self.layout.addWidget(self.port_label, self.layout.rowCount(), 0)
        self.layout.addWidget(self.port_edit, self.layout.rowCount() - 1, 1)

        self.format_label = QtWidgets.QLabel()
        self.format_edit = QtWidgets.QLineEdit(str(self.settings.value('socket/format')))
        self.layout.addWidget(self.format_label, self.layout.rowCount(), 0)
        self.layout.addWidget(self.format_edit, self.layout.rowCount() - 1, 1)

        self.path = self.settings.value('socket/path')
        self.path_label = QtWidgets.QLabel('.' + self.path[self.path[:-1].rfind('/'):])
        self.btn_path = QtWidgets.QPushButton()
        self.btn_path.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.btn_path.clicked.connect(self.show_dialog)
        self.layout.addWidget(self.path_label, self.layout.rowCount(), 0)
        self.layout.addWidget(self.btn_path, self.layout.rowCount() - 1, 1)

        self.log_prefix_label = QtWidgets.QLabel()
        self.log_prefix_edit = QtWidgets.QLineEdit(str(self.settings.value('socket/prefix')))
        self.layout.addWidget(self.log_prefix_label, self.layout.rowCount(), 0)
        self.layout.addWidget(self.log_prefix_edit, self.layout.rowCount() - 1, 1)

        self.log_title_label = QtWidgets.QLabel()
        self.log_title_edit = QtWidgets.QLineEdit(str(self.settings.value('socket/title')))
        self.layout.addWidget(self.log_title_label, self.layout.rowCount(), 0)
        self.layout.addWidget(self.log_title_edit, self.layout.rowCount() - 1, 1)

    def update_settings(self):
        self.update_setting(self.read_int_from_edit, self.port_edit, 'socket/port')
        self.settings.setValue('socket/format', self.format_edit.text())
        self.settings.setValue('socket/path', self.path)
        self.settings.setValue('socket/prefix', self.log_prefix_edit.text())
        self.settings.setValue('socket/title', self.log_title_edit.text() + '\n')

    def show_dialog(self):
        self.path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select directory', './telemetry_log/') + '/'
        self.path_label.setText('.' + self.path[self.path[:-1].rfind('/'):])


class Connection_properties_widget(Abstract_properties):
    def __init__(self, status_bar=None):
        super(Connection_properties_widget, self).__init__()
        self.status_bar = status_bar

        self.setup_ui()
        self.setup_ui_settings()

    def setup_ui_settings(self):
        self.data_object_label.setText(_('Data class'))
        self.packet_size_label.setText(_('Packet size'))
        self.state_check_box.setText(_('Enable States'))
        self.state_num_label.setText(_('State number'))

    def setup_ui(self):
        self.layout = QtWidgets.QGridLayout(self)

        self.data_object_label = QtWidgets.QLabel()
        self.data_object_combo_box = QtWidgets.QComboBox()
        self.data_object_combo_box.addItems(['log', 'socket'])
        self.data_object_combo_box.activated.connect(self.change_data_object_properties)
        self.layout.addWidget(self.data_object_label, self.layout.rowCount(), 0)
        self.layout.addWidget(self.data_object_combo_box, self.layout.rowCount() - 1, 1)
        self.property_row = self.layout.rowCount()
        self.set_data_object_properties()

        self.packet_size_label = QtWidgets.QLabel()
        self.packet_size_edit = QtWidgets.QLineEdit(str(self.settings.value('connection_widget/packet_size')))
        self.layout.addWidget(self.packet_size_label, self.layout.rowCount(), 0)
        self.layout.addWidget(self.packet_size_edit, self.layout.rowCount() - 1, 1)

        self.state_check_box = QtWidgets.QCheckBox()
        self.state_check_box.setTristate(False)
        self.state_check_box.setCheckState(self.num_bool_to_check_state(self.settings.value('connection_widget/board_state_is_on')))
        self.layout.addWidget(self.state_check_box, self.layout.rowCount(), 0, 1, 2)

        self.state_num_label = QtWidgets.QLabel()
        self.state_num_edit = QtWidgets.QLineEdit(str(self.settings.value('connection_widget/board_state_num')))
        self.layout.addWidget(self.state_num_label, self.layout.rowCount(), 0)
        self.layout.addWidget(self.state_num_edit, self.layout.rowCount() - 1, 1)

    def set_data_object_properties(self):
        self.property = None
        index = self.data_object_combo_box.currentIndex()
        if index == 0:
            self.property = Log_properties_widget(self.status_bar)
        elif index == 1:
            self.property = Socket_properties_widget(self.status_bar)
        self.layout.addWidget(self.property, self.property_row, 0, 1, 2)

    def change_data_object_properties(self):
        self.layout.removeWidget(self.property)
        self.set_data_object_properties()

    def update_settings(self):
        self.settings.setValue('connection_widget/data_class_name', self.data_object_combo_box.currentText())
        self.update_setting(self.read_int_from_edit, self.packet_size_edit, 'connection_widget/packet_size')
        self.settings.setValue('connection_widget/board_state_is_on', self.check_state_to_bool(self.state_check_box.checkState()))
        self.update_setting(self.read_int_from_edit, self.state_num_edit, 'connection_widget/board_state_num')

        try:
            self.settings.setValue('connection_widget/state_list', user_settings.STATE_LIST)
            self.settings.setValue('connection_widget/errors_list', user_settings.ERRORS_LIST)
        except Exception as e:
            self.exeption_action(e)
        self.property.update_settings()


class Settings_window(QtWidgets.QMainWindow):
    change_settings = QtCore.pyqtSignal()

    def __init__(self):
        super(Settings_window, self).__init__()
        self.settings = settings_ctrl.init_settings()

        self.setup_ui()
        self.setup_ui_settings()

    def setup_ui_settings(self):
        self.resize(int(self.settings.value('settings_window/size')[0]), int(self.settings.value('settings_window/size')[1]))
        self.setWindowTitle(_("Settings"))
        self.setPalette(palette.palette_list[self.settings.value('settings_window/palette')])

        self.properties.setup_ui_settings()

    def setup_ui(self):
        self.toolbar = self.addToolBar('Settings')

        self.main_properties_btn = self.toolbar.addAction(QtGui.QIcon(MAIN_PROPERTIES_ICON_PATH), 'Main properties')
        self.main_properties_btn.triggered.connect(self.set_main_properties)

        self.connection_properties_btn = self.toolbar.addAction(QtGui.QIcon(CONNECTION_PROPERTIES_ICON_PATH), 'Connectiono properties')
        self.connection_properties_btn.triggered.connect(self.set_connection_properties)

        self.graph_properties_btn = self.toolbar.addAction(QtGui.QIcon(GRAPH_PROPERTIES_ICON_PATH), 'Graph properties')
        self.graph_properties_btn.triggered.connect(self.set_graph_properties)

        self.model_properties_btn = self.toolbar.addAction(QtGui.QIcon(MODEL_PROPERTIES_ICON_PATH), 'Map properties')
        self.model_properties_btn.triggered.connect(self.set_model_properties)

        self.map_properties_btn = self.toolbar.addAction(QtGui.QIcon(MAP_PROPERTIES_ICON_PATH), 'Map properties')
        self.map_properties_btn.triggered.connect(self.set_map_properties)

        self.apply_btn = self.toolbar.addAction(QtGui.QIcon(ARROW_ICON_PATH), 'Apply')
        self.apply_btn.triggered.connect(self.apply_settings)
        self.set_main_properties()
        self.apply_btn_on = True

    def set_properties(self):
        self.statusBar().showMessage(_('Tab arrow to applay settings'))
        self.setCentralWidget(self.properties)

    def set_main_properties(self):
        self.properties = Main_properties_widget(self.statusBar())
        self.set_properties()

    def set_connection_properties(self):
        self.properties = Connection_properties_widget(self.statusBar())
        self.set_properties()

    def set_model_properties(self):
        self.properties = Model_properties_widget(self.statusBar())
        self.set_properties()

    def set_map_properties(self):
        self.properties = Map_properties_widget(self.statusBar())
        self.set_properties()

    def set_graph_properties(self):
        self.properties = Graph_properties_widget(self.statusBar())
        self.set_properties()

    def apply_btn_mode(self, mode):
        self.apply_btn_on = mode

    def apply_settings(self):
        if self.apply_btn_on:
            self.properties.update_settings()
            self.change_settings.emit()
        else:
            self.statusBar().showMessage(_('Disconnect to applay settings'))

    def show(self):
        self.hide()
        super(Settings_window, self).show()


class Data_manager(QtCore.QThread):
    new_data = QtCore.pyqtSignal(list)
    clear_all = QtCore.pyqtSignal()
    autoclose = QtCore.pyqtSignal()
    def __init__(self, data_obj):
        super(Data_manager, self).__init__()
        self.data_obj = data_obj
        self.mutex = QtCore.QMutex()
        self.close_flag = False
        self.daemon = True

    def change_data_obj(self, data_obj):
        if not self.isRunning():
            self.data_obj = data_obj
            return True
        else:
            return False

    def run(self):
        while True:
            self.mutex.lock()
            close = self.close_flag
            self.mutex.unlock()

            if close:
                break

            try:
                data = self.data_obj.read_data()
            except EOFError:
                self.autoclose.emit()
                break
            except Exception as e:
                print(e)
            else:
                self.new_data.emit(data)

    def open(self):
        self.new_data.emit(['BEG'])
        self.close_flag = False
        self.data_obj.start()
        self.start()

    def close(self):
        self.mutex.lock()
        self.close_flag = True
        self.mutex.unlock()

        self.exit()
        while self.isRunning():
            time.sleep(0.01)
            pass
        self.new_data.emit(['END'])
        self.data_obj.stop()


class Connection_widget(QtWidgets.QWidget):
    class Command_button(QtWidgets.QPushButton):
        def __init__(self, data_manager):
            super(Connection_widget.Command_button, self).__init__()
            self.connect = False
            self.setup_face()
            self.data_manager = data_manager
            self.clicked.connect(self.action)
            self.data_manager.autoclose.connect(self.autoclose_action)

        def setup_face(self):
            if self.connect:
                self.setText(_("Disconnect"))
            else:
                self.setText(_("Connect"))

        def action(self):
            if self.connect:
                self.data_manager.close()
                self.connect = False
            else:
                self.data_manager.open()
                self.connect = True

            self.setup_face()

        def autoclose_action(self):
            self.action()

    def __init__(self):
        super(Connection_widget, self).__init__()
        self.settings = settings_ctrl.init_settings()

        self.setAutoFillBackground(True)

        self.setup_ui()
        self.setup_ui_settings()

    def setup_ui(self):
        self.layout = QtWidgets.QGridLayout(self)

        self.states_status = []

        self.layout.setRowStretch(0, 40)

        self.data_manager = Data_manager(self.init_data_object())
        self.packet_count = 0

        self.state_list_label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.state_list_label, 1, 0, 1, 2)

        self.state_list = self.settings.value('connection_widget/state_list')
        self.error_list = self.settings.value('connection_widget/error_list')
        self.board_state_is_on = int(self.settings.value('connection_widget/board_state_is_on'))

        for state in self.state_list:
            self.layout.addWidget(QtWidgets.QLabel(state), self.layout.rowCount(), 0)
            self.states_status.append(QtWidgets.QLabel(_('None')))
            self.layout.addWidget(self.states_status[-1], self.layout.rowCount() - 1, 1)

        self.state_now_sep_label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.state_now_sep_label, self.layout.rowCount(), 0, 1, 2)
        self.state_now_label = QtWidgets.QLabel()
        self.layout.addWidget(self.state_now_label, self.layout.rowCount(), 0)
        self.state_now_value_label = QtWidgets.QLabel(_('None'))
        self.layout.addWidget(self.state_now_value_label, self.layout.rowCount() - 1, 1)

        self.connection_data_label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.connection_data_label, self.layout.rowCount(), 0, 1, 2)

        self.connection_type_label = QtWidgets.QLabel()
        self.layout.addWidget(self.connection_type_label, self.layout.rowCount(), 0)
        self.connection_type_value_label = QtWidgets.QLabel(self.settings.value('connection_widget/data_class_name'))
        self.layout.addWidget(self.connection_type_value_label, self.layout.rowCount() - 1, 1)

        self.packet_count_label = QtWidgets.QLabel()
        self.layout.addWidget(self.packet_count_label, self.layout.rowCount(), 0)
        self.packet_count_value_label = QtWidgets.QLabel(_('None'))
        self.layout.addWidget(self.packet_count_value_label, self.layout.rowCount() - 1, 1)

        self.btn_command = self.Command_button(self.data_manager)
        self.btn_command.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.layout.addWidget(self.btn_command, self.layout.rowCount(), 0)

        self.btn_clear = QtWidgets.QPushButton()
        self.btn_clear.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.btn_clear.clicked.connect(self.btn_clear_action)
        self.layout.addWidget(self.btn_clear, self.layout.rowCount() - 1, 1)

        self.layout.setRowStretch(self.layout.rowCount(), 40)

    def setup_ui_settings(self):
        self.state_list_label.setText(_('==================\nState list\n=================='))
        self.state_now_sep_label.setText(_('----------------------------------------'))
        self.state_now_label.setText(_('State now'))
        self.connection_data_label.setText(_('==================\nConnection data\n =================='))
        self.connection_type_label.setText(_('Connection type'))
        self.connection_type_value_label.setText(self.settings.value('connection_widget/data_class_name'))
        self.packet_count_label.setText(_('Packet count'))

        self.data_manager.change_data_obj(self.init_data_object())
        self.btn_command.setup_face()
        self.btn_clear.setText(_("Clear"))

    def init_data_object(self):
        try:
            if self.settings.value('connection_widget/data_class_name') == 'log':
                real_time = bool(int(self.settings.value('log/real_time')))
                obj = log_data.Data_source(self.settings.value('log/path'),
                                           real_time,
                                           float(self.settings.value('log/time_delay')))
            elif self.settings.value('connection_widget/data_class_name') == 'socket':
                obj = socket_data.Data_source(int(self.settings.value('socket/port')),
                                              self.settings.value('socket/format'),
                                              self.settings.value('socket/path') + self.settings.value('socket/prefix'),
                                              self.settings.value('socket/title'))
        except Exception as e:
            obj = None
            print(e)
        return obj

    def new_data_reaction(self, data):
        if data[0] == 'BEG':
            self.board_state_is_on = int(self.settings.value('connection_widget/board_state_is_on'))
            self.board_state_num = int(self.settings.value('connection_widget/board_state_num'))
            self.clear_data()

        elif data[0] != 'END':
            self.packet_count += 1
            self.packet_count_value_label.setText(str(self.packet_count))

            if self.board_state_is_on:
                state_now = trunc(data[self.board_state_num])

                if state_now >= len(self.states_status):
                    if state_now >= len(self.states_status) + len(self.error_list):
                        self.state_now_value_label.setText(_('Unknown state'))
                    else:
                        self.state_now_value_label.setText(self.error_list[state_now - len(self.states_status)])
                elif self.state_now_value_label.text() != self.state_list[state_now]:
                    for i in range(len(self.states_status)):
                        if i < state_now:
                            self.states_status[i].setText(_('Terminated'))
                        elif i == state_now:
                            self.states_status[i].setText(_('Running'))
                        else:
                            self.states_status[i].setText(_('Waiting'))
                    self.state_now_value_label.setText(self.state_list[state_now])

    def clear_data(self):
        if self.board_state_is_on:
            for state in self.states_status:
                state.setText(_('None'))
            self.state_now_value_label.setText(_('None'))
        else:
            for state in self.states_status:
                state.setText(_('------'))
            self.state_now_value_label.setText(_('------'))
        self.packet_count = 0
        self.packet_count_value_label.setText(str(self.packet_count))

    def btn_clear_action(self):
        self.btn_command.data_manager.clear_all.emit()


class Graph_widget(PG.GraphicsLayoutWidget):
    class Curve():
        def __init__(self, plot, pen, data_extractor, number):
            self.number = number
            self.plot = plot
            self.pen = pen
            self.data_extractor = data_extractor
            self.arr = None
            self.curve = None

        def show_data(self, data):
            if self.arr is None:
                self.arr = NumPy.array([data[0], self.data_extractor(data[self.number])])
                if self.curve is None:
                    self.curve = self.plot.plot(self.arr, pen=self.pen)
                    return
            else:
                self.arr = NumPy.vstack((self.arr, NumPy.array([data[0], self.data_extractor(data[self.number])])))
            self.curve.setData(self.arr)

        def clear(self):
            self.arr = None

    def __init__(self):
        super(Graph_widget, self).__init__()
        self.settings = settings_ctrl.init_settings()

        self.setup_ui()
        self.setup_ui_settings()

    def setup_ui(self):
        self.all_curves = []
        self.all_plots = []

    def setup_ui_settings(self):
        for plot in self.all_plots:
            self.removeItem(plot)
        self.setup_ui()

        self.settings.beginGroup('graph_widget')
        self.automatic_position = int(self.settings.value('automatic_position'))
        self.column = 0
        self.row = 0
        self.settings.beginGroup("graph")
        self.settings.setValue("acceleration/name", _("Acceleration"))
        self.settings.setValue("gyro/name", _("Gyro"))
        self.settings.setValue("pressure/name", _("Pressure"))
        self.settings.setValue("temperature/name", _("Temperature"))
        self.settings.setValue("mag/name", _("Mag"))
        self.settings.setValue("lux/name", _("Lux"))
        self.settings.setValue("voltage/name", _("Voltage"))
        self.settings.setValue("altitude/name", _("Altitude"))
        for group in self.settings.childGroups():
            self.settings.beginGroup(group)
            if self.settings.value("is_on"):
                if not self.automatic_position:
                    self.setup_graph(self.settings.value("num"), self.settings.value("converter"),
                                     self.settings.value("position"), self.settings.value("colour"),
                                     self.settings.value("name"))
                else:
                    self.setup_graph(self.settings.value("num"), self.settings.value("converter"),
                                     [self.row, self.column], self.settings.value("colour"),
                                     self.settings.value("name"))
                    self.row += 1
                    if self.row >= 3:
                        self.row = 0
                        self.column += 1

            self.settings.endGroup()
        self.settings.endGroup()
        self.settings.endGroup()

    def setup_graph(self, num, converter, position, colour, name):
        axis_x = PG.AxisItem(orientation='left')
        axis_x.setLabel(name)
        axis_y = PG.AxisItem(orientation='bottom')
        axis_y.setLabel(_("Time"))
        plot = self.addPlot(row=position[0], col=position[1], axisItems={'left': axis_x, 'bottom': axis_y})

        curves = []
        for i in range(len(num)):
            curves = curves + [self.Curve(plot, colour[i], converter[i], num[i])]

        self.all_curves += curves
        self.all_plots += [plot]

    def new_data_reaction(self, data):
        if data[0] == 'BEG':
            self.clear_data()
        elif data[0] != 'END':
            for curve in self.all_curves:
                curve.show_data(data)

    def clear_data(self):
        for curve in self.all_curves:
            curve.clear()


class Model_widget(OpenGL.GLViewWidget):
    def __init__(self):
        super(Model_widget, self).__init__()
        self.settings = settings_ctrl.init_settings()

        self.setAutoFillBackground(True)

        self.original_nadir_vector = NumPy.array([1, 1, -1], dtype='double')
        self.original_nadir_vector /= NumPy.linalg.norm(self.original_nadir_vector)

        self.setup_ui()
        self.setup_ui_settings()

    def setup_ui(self):
        self.gird = OpenGL.GLGridItem()
        self.gird.scale(2, 2, 2)
        self.gird.translate(0, 0, -2)
        self.addItem(self.gird)

        verts = self._get_mesh_points(MESH_PATH)
        faces = NumPy.array([(i, i + 1, i + 2,) for i in range(0, len(verts), 3)])

        self.mesh = OpenGL.GLMeshItem(vertexes=verts, faces=faces, faceColors=satellite_model.colors, smooth=False, shader='edgeHilight', computeNormals=True)
        self.addItem(self.mesh)

    def setup_ui_settings(self):
        self.setCameraPosition(distance=25, elevation=20, azimuth=270)
        self.data_converter = self.settings.value('model_widget/converter')
        self.model_num = []
        for num in self.settings.value('model_widget/num'):
            self.model_num.append(int(num))

    def _get_mesh_points(self, mesh_path):
        mesh = StlMesh.Mesh.from_file(mesh_path)
        points = mesh.points
        points = NumPy.array(list(chain(*points)))
        nd_points = NumPy.ndarray(shape=(len(points) // 3, 3,))
        i = 0
        for i in range(0, len(points) // 3):
            nd_points[i] = points[i * 3: (i + 1) * 3]
        return nd_points

    def _update_mesh_angles(self, angles):
        self.clear_data()
        self.rotate_object(self.mesh, angles[1], [-1, 0, 0])
        self.rotate_object(self.mesh, angles[0], [0, 1, 0])
        self.rotate_object(self.mesh, angles[2], [0, 0, -1])

    def rotate_object(self, obj, angle, axis):
        obj.rotate(angle, axis[0], axis[1], axis[2])

    def new_data_reaction(self, data):
        if data[0] == 'BEG':
            self.model_num = []
            self.data_converter = self.settings.value('model_widget/converter')
            self.model_num = []
            for num in self.settings.value('model_widget/num'):
                self.model_num.append(int(num))
        elif data[0] != 'END':
            angles = []
            for i in range(3):
                angles.append(self.data_converter[i](data[self.model_num[i]]))
            self._update_mesh_angles(angles)

    def clear_data(self):
        self.mesh.resetTransform()


class Map_widget(QtWidgets.QDialog):
    def __init__(self):
        super(Map_widget, self).__init__()
        self.settings = settings_ctrl.init_settings()

        self.setup_ui()
        self.setup_ui_settings()

    def setup_ui(self):
        self.layout = QtWidgets.QGridLayout(self)

        self.map = Open_street_map()
        self.layout.addWidget(self.map)
        self.map.waitUntilReady()
        self.previous_data = []
        self.keys = []
        self.key_num = 1
        self.data_threat = False
        self.data_converter = self.settings.value('map_widget/converter')
        self.position_num = []
        for num in self.settings.value('map_widget/num'):
            self.position_num.append(int(num))

    def setup_ui_settings(self):
        self.map.centerAt(float(self.settings.value('map_widget/center')[0]),
                          float(self.settings.value('map_widget/center')[1]))
        self.map.setZoom(int(self.settings.value('map_widget/zoom')))

    def new_data_reaction(self, data):
        if data[0] == 'BEG':
            self.clear_data()
        elif data[0] != 'END':
            self.map.centerAt(self.data_converter(data[self.position_num[0]]),
                              self.data_converter(data[self.position_num[1]]))
            if (self.keys == []):
                self.data_converter = self.settings.value('map_widget/converter')
                for num in self.settings.value('map_widget/num'):
                    self.position_num.append(int(num))
                self.previous_data = data
                self.keys.append(self.map.addMarker(str(0), latitude=self.data_converter(data[self.position_num[0]]),
                                                    longitude=self.data_converter(data[self.position_num[1]]),
                                                    **dict(icon=ICON_PATH_ACTIVE, title="Position now")))
                self.map.centerAt(self.data_converter(data[self.position_num[0]]), self.data_converter(data[self.position_num[1]]))
                return

            self.keys.append(self.map.addMarker(str(self.key_num), latitude=self.data_converter(self.previous_data[self.position_num[0]]),
                                                longitude=self.data_converter(self.previous_data[self.position_num[1]]),
                                                **dict(icon=ICON_PATH_PASSIVE, title=str(self.previous_data[0]))))
            self.map.moveMarker(str(0), latitude=self.data_converter(data[self.position_num[0]]),
                                longitude=self.data_converter(data[self.position_num[1]]))
            self.previous_data = data
            self.key_num += 1                

    def clear_data(self):
        for key in self.keys:
            self.map.runScript("delete_marker(key={!r})".format(key))
        self.keys = []
        self.key_num = 1


class Central_widget(QtWidgets.QWidget):
    def __init__(self):
        super(Central_widget, self).__init__()
        self.settings = settings_ctrl.init_settings()

        self.setup_ui()
        self.setup_ui_settings()

    def setup_ui(self):
        self.layout = QtWidgets.QGridLayout(self)

        self.data_dependent_widgets = []

        if int(self.settings.value('graph_widget/is_on')):
            self.graph_widget = Graph_widget()
            self.data_dependent_widgets.append(self.graph_widget)
            if int(self.settings.value('map_widget/is_on')) and int(self.settings.value('model_widget/is_on')):
                self.layout.addWidget(self.graph_widget, 0, 0, 1, 2)
            else:
                self.layout.addWidget(self.graph_widget, 0, 0)

        if int(self.settings.value('model_widget/is_on')):
            self.model_widget = Model_widget()
            self.data_dependent_widgets.append(self.model_widget)
            if not int(self.settings.value('graph_widget/is_on')):
                self.layout.addWidget(self.model_widget, 0, 0)
            else:
                self.layout.addWidget(self.model_widget, self.layout.rowCount(), 0)

        if int(self.settings.value('map_widget/is_on')):
            self.map_widget = Map_widget()
            self.data_dependent_widgets.append(self.map_widget)
            if int(self.settings.value('model_widget/is_on')):
                self.layout.addWidget(self.map_widget, self.layout.rowCount() - 1, 1)
            elif not int(self.settings.value('graph_widget/is_on')):
                self.layout.addWidget(self.map_widget, 0, 0)
            else:
                self.layout.addWidget(self.map_widget, self.layout.rowCount(), 0)

        for i in range(self.layout.rowCount())[:]:
            self.layout.setRowMinimumHeight(i, 30)
            self.layout.setRowStretch(i, 40)
        for i in range(self.layout.columnCount())[:]:
            self.layout.setColumnMinimumWidth(i, 40)
            self.layout.setColumnStretch(i, 30)

        self.connection_widget = Connection_widget()
        self.data_dependent_widgets.append(self.connection_widget)
        self.layout.addWidget(self.connection_widget, 0, self.layout.columnCount(), self.layout.rowCount(), 1)

    def setup_ui_settings(self):
        for widget in self.data_dependent_widgets:
            widget.setup_ui_settings()

    def new_data_reaction(self, data):
        if data[0] == 'BEG':
            self.clear_all()
        for widget in self.data_dependent_widgets:
            widget.new_data_reaction(data)

    def clear_all(self):
        for widget in self.data_dependent_widgets:
            widget.clear_data()


class Main_window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main_window, self).__init__()
        self.settings = settings_ctrl.init_settings()

        if not settings_ctrl.check_settings(self.settings):
            settings_ctrl.reset_to_default(self.settings)

        settings_ctrl.reset_to_default(self.settings)# OFT <<<<<<<<
        self.change_lng()

        self.move_to_center()
        self.setWindowIcon(QtGui.QIcon(ICON_PATH))

        self.setup_ui()
        self.setup_ui_settings()

    def setup_ui_settings(self):
        self.change_lng()

        self.resize(int(self.settings.value('main_window/size')[0]), int(self.settings.value('main_window/size')[1]))
        self.setWindowTitle(_("StrelA"))
        self.setPalette(palette.palette_list.get(self.settings.value('settings_window/palette')))
        self.statusBar().showMessage(_("Welcome"))
        self.menu_file.setTitle(_("&File"))
        self.action_settings.setText(_("&Settings"))
        self.action_settings.setStatusTip(_("Settings"))
        self.action_exit.setText(_("&Exit"))
        self.action_exit.setStatusTip(_("Exit"))

    def setup_ui(self):
        self.settings_window = Settings_window()
        self.settings_window.change_settings.connect(self.change_settings)

        self.menu_bar = self.menuBar()

        self.menu_file = self.menu_bar.addMenu(_("&File"))

        self.action_settings = self.menu_file.addAction(_("&Settings"))
        self.action_settings.setShortcut('Ctrl+S')
        self.action_settings.triggered.connect(self.settings_window.show)

        self.action_exit = self.menu_file.addAction(_("&Exit"))
        self.action_exit.setShortcut('Ctrl+Q')
        self.action_exit.triggered.connect(QtWidgets.qApp.quit)

        self.central_widget = Central_widget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.connection_widget.btn_command.data_manager.new_data.connect(self.new_data_reaction)
        self.central_widget.connection_widget.btn_command.data_manager.clear_all.connect(self.clear_all)

    def change_settings(self):
        self.setup_ui_settings()
        self.settings_window.setup_ui_settings()
        self.central_widget.setup_ui_settings()

    def new_data_reaction(self, data):
        print(data)
        if data[0] == 'BEG':
            self.settings_window.apply_btn_mode(False)
            self.central_widget.new_data_reaction(data)
        elif data[0] == 'END':
            self.settings_window.apply_btn_mode(True)
            self.central_widget.new_data_reaction(data)
        elif len (data) == int(self.settings.value('connection_widget/packet_size')):
            self.central_widget.new_data_reaction(data)
        else:
            self.statusBar().showMessage(_('Wrong data packet'))

    def clear_all(self):
        self.central_widget.clear_all()
        self.statusBar().showMessage('')

    def change_lng(self, lng=None):
        if lng is None:
            lng = self.settings.value('language')
        lng = gettext.translation('sourse', localedir='./sourse/language', languages=[lng])
        lng.install()

    def move_to_center(self):
        frame = self.frameGeometry()
        frame.moveCenter(QtWidgets.QDesktopWidget().availableGeometry().center())
        self.move(frame.topLeft())

    def closeEvent(self, evnt):
        self.settings_window.close()
        super(Main_window, self).closeEvent(evnt)
