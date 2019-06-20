import time

from PyQt5 import QtCore, QtWidgets, QtGui
import pyqtgraph as PG
import pyqtgraph.opengl as OpenGL

import numpy as NumPy
from stl import mesh as StlMesh
from itertools import chain
from math import acos, trunc

from sourse.map_sourse.PyQtMap import Open_street_map

import gettext

from config import *
from sourse.data_class import log_data
from sourse.data_class import socket_data
from satellite_model import *
from sourse.exceptions import *
from sourse.settings_update import *

ICON_PATH = "./strela_icon.png"


MESH_PATH = './satellite_model_new.stl'

ICON_PATH_PASSIVE = "http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_gray.png"
ICON_PATH_ACTIVE = "http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_red.png"

LANGUAGE = ''
COLOUR_THEME = 'dark'

if LANGUAGE == "ru":
    lng = gettext.translation('sourse', localedir='./sourse/language', languages=['ru'])
    lng.install()
else:
    _ = lambda x: x

class Data_manager(QtCore.QThread):
    new_data = QtCore.pyqtSignal(list)
    clear_all = QtCore.pyqtSignal()
    autoclose = QtCore.pyqtSignal()

    def __init__(self, data_obj):
        super(Data_manager, self).__init__()
        self.data_obj = data_obj
        self.mutex = QtCore.QMutex()
        self.close_flag = False

    def change_data_obj(self, data_obj):
        if not self.isRunning():
            self.data_obj = data_obj
            return True
        else:
            return False

    def run(self):
        while True:
            self.mutex.lock()
            if self.close_flag is True:
                self.mutex.unlock()
                break
            self.mutex.unlock()

            try:
                data = self.data_obj.read_data()
            except DataThreadEnd:
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
        self.clear_all.emit()


class Connection_widget(QtWidgets.QWidget):

    class Command_button(QtWidgets.QPushButton):
        STATUS_DISCONNECT = 0
        STATUS_CONNECT = 1

        def __init__(self, data_manager):
            super(Connection_widget.Command_button, self).__init__()
            self.status = self.STATUS_DISCONNECT
            self.setup_face()
            self.data_manager = data_manager
            self.clicked.connect(self.action)
            self.data_manager.autoclose.connect(self.autoclose_action)

        def setup_face(self):
            if self.status == self.STATUS_CONNECT:
                self.setText(_("Disconnect"))
            elif self.status == self.STATUS_DISCONNECT:
                self.setText(_("Connect"))

        def action(self):
            if self.status == self.STATUS_CONNECT:
                self.data_manager.close()
                self.status = self.STATUS_DISCONNECT

            elif self.status == self.STATUS_DISCONNECT:
                self.data_manager.open()
                self.status = self.STATUS_CONNECT

            self.setup_face()

        def autoclose_action(self):
            self.action()

    def __init__(self, settings):
        super(Connection_widget, self).__init__()
        self.settings = settings


        self.setAutoFillBackground(True)
        self.setPalette(self.settings.value('connection_widget/palette'))

        self.data_manager = Data_manager(self.settings.value('connection_widget/data_class'))
        self.packet_count = 0

        self.setup_ui()

    def setup_ui(self):
        # Layout
        # ======================================================================
        self.layout = QtGui.QGridLayout(self)

        self.states_status = []

        # Labels
        # ======================================================================
        self.layout.addWidget(QtWidgets.QLabel(_('==================\nState list\n=================='), alignment=QtCore.Qt.AlignHCenter), 1, 0, 1, 2)

        for i in STATE_LIST:
            self.layout.addWidget(QtWidgets.QLabel(i), self.layout.rowCount(), 0)
            self.states_status.append(QtWidgets.QLabel(_('None'), alignment=QtCore.Qt.AlignHCenter))
            self.layout.addWidget(self.states_status[-1], self.layout.rowCount() - 1, 1)

        self.layout.addWidget(QtWidgets.QLabel(_('----------------------------------------'), alignment=QtCore.Qt.AlignHCenter), self.layout.rowCount(), 0, 1, 2)

        self.layout.addWidget(QtWidgets.QLabel(_('State now')), self.layout.rowCount(), 0)
        self.state_now_lbl = (QtWidgets.QLabel(_('None'), alignment=QtCore.Qt.AlignHCenter))
        self.layout.addWidget(self.state_now_lbl, self.layout.rowCount() - 1, 1)

        self.layout.addWidget(QtWidgets.QLabel(_('==================\nConnection data\n =================='), alignment=QtCore.Qt.AlignHCenter), self.layout.rowCount(), 0, 1, 2)

        self.layout.addWidget(QtWidgets.QLabel(_('Connection type')), self.layout.rowCount(), 0)
        self.connection_type_lbl = (QtWidgets.QLabel(_('Log reply'), alignment=QtCore.Qt.AlignHCenter))
        self.layout.addWidget(self.connection_type_lbl, self.layout.rowCount() - 1, 1)

        self.layout.addWidget(QtWidgets.QLabel(_('Packet count')), self.layout.rowCount(), 0)
        self.packet_count_lbl = (QtWidgets.QLabel(_('None'), alignment=QtCore.Qt.AlignHCenter))
        self.layout.addWidget(self.packet_count_lbl, self.layout.rowCount() - 1, 1)

        # Push buttons
        # ======================================================================
        # Command
        # ----------------------------------------------------------------------
        self.btn_command = self.Command_button(self.data_manager)
        #self.btn_command.setPalette(self.palette.button())
        self.btn_command.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.layout.addWidget(self.btn_command, self.layout.rowCount(), 0)

        # Clear
        # ----------------------------------------------------------------------
        self.btn_clear = QtGui.QPushButton(_("Clear"))
        #self.btn_clear.setPalette(self.palette.button())
        self.btn_clear.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.layout.addWidget(self.btn_clear, self.layout.rowCount() - 1, 1)
        self.btn_clear.clicked.connect(self.btn_clear_action)

        self.layout.setRowStretch(0, 2)
        self.layout.setRowStretch(self.layout.rowCount(), 2)

    def new_data_reaction(self, data):
        if data[0] == 'BEG':
            for i in self.states_status:
                i.setText(_('Waiting'))
            return

        self.packet_count += 1
        self.packet_count_lbl.setText(str(self.packet_count))

        if BOARD_STATE:
            state = data[BOARD_STATE_NUMBER]
            state = trunc(state)

            if self.states_status[state].text() == _('None'):
                for i in self.states_status:
                    i.setText(_('Waiting'))

            if state >= len(STATE_LIST):
                if state >= (len(STATE_LIST) + len(ERRORS_LIST)):
                    self.state_now_lbl.setText(_('Unknown state'))
                else:
                    self.state_now_lbl.setText(ERRORS_LIST[state - len(STATE_LIST)])
                return
            elif self.states_status[state].text() == _('Waiting'):
                for i in range(state):
                    self.states_status[i].setText(_('Terminated'))
                self.states_status[state].setText(_('Running'))
                self.state_now_lbl.setText(STATE_LIST[state])

    def clear_data(self):
        for i in self.states_status:
            i.setText(_('None'))
        self.state_now_lbl.setText(_('None'))
        self.packet_count = 0
        self.packet_count_lbl.setText(_('None'))

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

    def __init__(self, settings):
        super(Graph_widget, self).__init__()
        self.settings = settings

        self.setup_graphs()

    def setup_graphs(self):
        self.all_curves = []
        self.all_plots = []
        converter = set_converters()

        self.settings.beginGroup('graph_widget')
        self.settings.setValue("accel_graph/name", _("Acceleration"))
        self.settings.setValue("gyro_graph/name", _("Gyro"))
        self.settings.setValue("pressure_graph/name", _("Pressure"))
        self.settings.setValue("temperature_graph/name", _("Temperature"))
        self.settings.setValue("mag_graph/name", _("Mag"))
        self.settings.setValue("voltage_graph/name", _("Lux"))
        for i in self.settings.childGroups():
            self.settings.beginGroup(i)
            if self.settings.value("is_on"):
                self.setup_graph(self.settings.value("num"), converter[i],
                                 self.settings.value("position"), self.settings.value("colour"),
                                 self.settings.value("name"))
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
            curves = curves + [self.Curve(plot, colour[i], converter, num[i])]

        self.all_curves += curves
        self.all_plots += [plot]

    def new_data_reaction(self, data):
        for curve in self.all_curves:
            curve.show_data(data)

    def clear_data(self):
        for curve in self.all_curves:
            curve.clear()


class Map_widget(QtWidgets.QDialog):
    def __init__(self):
        super(Map_widget, self).__init__()
        self.data_converter = GPS_CONVERTER

        self.setup_ui()
    
    def setup_ui(self):
        # Layout
        # ======================================================================
        self.layout = QtGui.QGridLayout(self)

        # Map
        # ======================================================================
        self.map = Open_street_map()
        self.layout.addWidget(self.map)

        self.map.waitUntilReady()

        self.map.centerAt(MAP_DEFAULT_CENTER[0], MAP_DEFAULT_CENTER[1])
        self.map.setZoom(MAP_DEFAULT_ZOOM)

        self.previous_data = []
        self.keys = []
        self.key_num = 1
        self.data_threat = False

    def new_data_reaction(self, data):
        if self.keys == []:
            self.previous_data = data
            self.keys.append(self.map.addMarker(str(0), 
                                                latitude=self.data_converter(data[GPS_NUMBER[0]]),
                                                longitude=self.data_converter(data[GPS_NUMBER[1]]),
                                                **dict(icon=ICON_PATH_ACTIVE,
                                                title="Position now")))
            self.map.centerAt(self.data_converter(data[GPS_NUMBER[0]]), self.data_converter(data[GPS_NUMBER[1]]))


        self.keys.append(self.map.addMarker(str(self.key_num),
                                            latitude=self.data_converter(self.previous_data[GPS_NUMBER[0]]),
                                            longitude=self.data_converter(self.previous_data[GPS_NUMBER[1]]),
                                            **dict(icon=ICON_PATH_PASSIVE, title=str(self.previous_data[0]))))
        self.map.moveMarker(str(0),
                            latitude=self.data_converter(data[GPS_NUMBER[0]]),
                            longitude=self.data_converter(data[GPS_NUMBER[1]]))
        self.previous_data = data
        self.key_num += 1                  

    def clear_data(self):
        for key in self.keys:
            self.map.runScript("delete_marker(key={!r})".format(key))
        self.keys = []
        self.key_num = 1


class Model_widget(OpenGL.GLViewWidget):
    def __init__(self, settings):
        super(Model_widget, self).__init__()
        self.settings = settings
        self.setup_ui()
        self.original_nadir_vector = NumPy.array([1, 1, -1], dtype='double')
        self.original_nadir_vector /= NumPy.linalg.norm(self.original_nadir_vector)

    def setup_ui(self):
        self.gird = OpenGL.GLGridItem()
        self.gird.scale(2, 2, 2)
        self.gird.translate(0, 0, -2)
        self.addItem(self.gird)

        self.setCameraPosition(distance=25, elevation=20, azimuth=270)

        verts = self._get_mesh_points(MESH_PATH)
        faces = NumPy.array([(i, i + 1, i + 2,) for i in range(0, len(verts), 3)])

        self.mesh = OpenGL.GLMeshItem(vertexes=verts, faces=faces, faceColors=colors, smooth=False, shader='edgeHilight', computeNormals=True)
        self.addItem(self.mesh)

    def _get_mesh_points(self, mesh_path):
        mesh = StlMesh.Mesh.from_file(mesh_path)
        points = mesh.points

        points = NumPy.array(list(chain(*points)))
        nd_points = NumPy.ndarray(shape=(len(points) // 3, 3,))

        i = 0
        for i in range(0, len(points) // 3):
            nd_points[i] = points[i * 3: (i + 1) * 3]

        return nd_points

    def _update_mesh_vector(self, new_nadir_vector):

        new_nadir_vector = NumPy.array(new_nadir_vector, dtype='double')
        new_nadir_vector /= NumPy.linalg.norm(new_nadir_vector)

        angle = acos(NumPy.dot(self.original_nadir_vector, new_nadir_vector))
        angle = angle * 180 / NumPy.pi
        axis = NumPy.cross(self.original_nadir_vector, new_nadir_vector)
        self.clear_data()
        self.rotate_object(self.mesh, angle, axis)

    def _update_mesh_angles(self, angles):
        self.clear_data()
        self.rotate_object(self.mesh, angles[1], [-1, 0, 0])
        self.rotate_object(self.mesh, angles[0], [0, 1, 0])
        self.rotate_object(self.mesh, angles[2], [0, 0, -1])

    def rotate_object(self, obj, angle, axis):
        obj.rotate(angle, axis[0], axis[1], axis[2])

    def new_data_reaction(self, data):
        self._update_mesh_angles([data[MODEL_NUMBER[0]], data[MODEL_NUMBER[1]], data[MODEL_NUMBER[2]]])

    def clear_data(self):
        self.mesh.resetTransform()

class Command_line_widget(QtGui.QWidget):
    def __init__(self):
        super(Command_line_widget, self).__init__()

        self.setAutoFillBackground(True)
        self.setup_ui()

    def setup_ui(self):
        # Layout
        # ======================================================================
        self.layout = QtGui.QGridLayout(self)

        # Line edit
        # ======================================================================
        self.line_edit = QtGui.QLineEdit()
        self.layout.addWidget(self.line_edit, 0, 0)

        # Button enter
        # ======================================================================
        self.btn_send = QtGui.QPushButton(_("Send"))
        self.btn_send.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.btn_send.clicked.connect(self.send_action)
        self.layout.addWidget(self.btn_send, 0, 1)

    def send_action(self):
        print (self.line_edit.text())
        self.line_edit.clear()


class Central_widget(QtGui.QWidget):
    def __init__(self, settings):
        super(Central_widget, self).__init__()
        self.settings = settings
        
        self.setAutoFillBackground(True)
        self.setPalette(self.settings.value('central_widget/palette'))

        self.data_threat = False

        self.setup_ui()

    def setup_ui(self):
        # Layout
        # ======================================================================
        self.layout = QtGui.QGridLayout(self)

        # Widgets
        # ======================================================================
        self.data_dependent_widgets = []

        # Graphs
        # ----------------------------------------------------------------------
        if self.settings.value('graph_widget/is_on'):
            self.graphs_widget = Graph_widget(self.settings)
            if self.settings.value('map_widget/is_on') and self.settings.value('model_widget/is_on'):
                self.layout.addWidget(self.graphs_widget, 0, 0, 1, 2)
            else:
                self.layout.addWidget(self.graphs_widget, 0, 0)
            self.data_dependent_widgets.append(self.graphs_widget)

        # Model
        # ----------------------------------------------------------------------
        if self.settings.value('model_widget/is_on'):
            self.model_widget = Model_widget(self.settings)
            if not self.settings.value('graph_widget/is_on'):
                self.layout.addWidget(self.model_widget, 0, 0)
            else:
                self.layout.addWidget(self.model_widget, self.layout.rowCount(), 0)
            self.data_dependent_widgets.append(self.model_widget)

        # Map
        # ----------------------------------------------------------------------
        if self.settings.value('map_widget/is_on'):
            self.map_widget = Map_widget()
            if self.settings.value('model_widget/is_on'):
                self.layout.addWidget(self.map_widget, self.layout.rowCount() - 1, 1)
            elif not self.settings.value('graph_widget/is_on'):
                self.layout.addWidget(self.map_widget, 0, 0)
            else:
                self.layout.addWidget(self.map_widget, self.layout.rowCount(), 0)
            self.data_dependent_widgets.append(self.map_widget)

        # Layout stretch
        # ======================================================================
        for i in range(self.layout.rowCount()):
            self.layout.setRowMinimumHeight(i, 30)
            self.layout.setRowStretch(i, 40)
        for i in range(self.layout.columnCount()):
            self.layout.setColumnMinimumWidth(i, 40)
            self.layout.setColumnStretch(i, 30)

        # Connection
        # ----------------------------------------------------------------------
        self.connection_widget = Connection_widget(self.settings)
        if not (self.settings.value('graph_widget/is_on') or self.settings.value('map_widget/is_on') or self.settings.value('model_widget/is_on')):
            self.layout.addWidget(self.connection_widget, 0, 0)
        elif self.layout.rowCount() == 1:
            self.layout.addWidget(self.connection_widget, 0, self.layout.columnCount())
        else:
            self.layout.addWidget(self.connection_widget, 0, self.layout.columnCount(), 2, 1)
        self.data_dependent_widgets.append(self.connection_widget)

        # Command line
        # ----------------------------------------------------------------------
        if self.settings.value('command_line_widget/is_on'):
            self.command_line_widget = Command_line_widget()
            self.layout.addWidget(self.command_line_widget, self.layout.rowCount(), 0, 1, self.layout.columnCount())

        # Interconnection
        # ======================================================================
        self.connection_widget.btn_command.data_manager.new_data.connect(self.new_data_reaction)
        self.connection_widget.btn_command.data_manager.clear_all.connect(self.clear_all)


    def new_data_reaction(self, data):
        if data[0] == 'BEG':
            self.data_threat = True
            self.clear_all()
            return
        elif data[0] == 'END':
            self.data_threat = False
            return
        if self.data_threat:
            for widget in self.data_dependent_widgets:
                widget.new_data_reaction(data)

    def clear_all(self):
        for widget in self.data_dependent_widgets:
            widget.clear_data()


class Settings_widget(QtGui.QDialog):
    def __init__(self, settings):
        super(Settings_widget, self).__init__()
        self.settings = settings

        self.resize(self.settings.value('settings_window/size')[0], self.settings.value('settings_window/size')[1])

        self.setWindowTitle(_("Settings"))
        self.setup_ui()

    def setup_ui(self):
        # Layout
        # ======================================================================
        self.layout = QtGui.QGridLayout(self)

        # Line edit
        # ======================================================================
        self.select_data_class = QtGui.QComboBox()
        self.layout.addWidget(self.select_data_class, 0, 0)

        # Button enter
        # ======================================================================
        self.btn_send = QtGui.QPushButton(_("Enter"))
        self.btn_send.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.btn_send.clicked.connect(self.send_action)
        self.layout.addWidget(self.btn_send, 0, 1)

    def send_action(self):
        print (self.line_edit.text())
        self.line_edit.clear()


class Main_window(QtGui.QMainWindow):
    def __init__(self):
        super(Main_window, self).__init__()
        self.settings = QtCore.QSettings("Agnus", "StrelA")
        self.settings.Format(QtCore.QSettings.IniFormat)
        self.settings.Scope(QtCore.QSettings.UserScope)
        self.settings_window = None

        update_settings(self.settings)

        self.resize(self.settings.value('main_window/size')[0], self.settings.value('main_window/size')[1])
        self.move_to_center()
        self.setWindowTitle(_("StrelA"))
        self.setWindowIcon(QtGui.QIcon(ICON_PATH))
        self.setPalette(self.settings.value('main_window/palette'))
        self.statusBar().showMessage(_("Welcome"))

        self.setup_ui()

    def setup_ui(self):

        # Central widget
        # ======================================================================
        self.central_widget = Central_widget(self.settings)
        self.setCentralWidget(self.central_widget)

        # Menu Bar
        # ======================================================================
        self.menu_bar = self.menuBar()

        #File
        # ----------------------------------------------------------------------
        menu_file = self.menu_bar.addMenu(_("&File"))

        action_exit = QtGui.QAction(_("&Exit"), self)
        action_exit.setShortcut('Ctrl+Q')
        action_exit.setStatusTip(_("Exit"))
        action_exit.triggered.connect(QtWidgets.qApp.quit)

        menu_file.addAction(action_exit)

        # Tools
        # ----------------------------------------------------------------------
        menu_tools = self.menu_bar.addMenu(_("&Tools"))
        action_settings = QtGui.QAction(_("&Settings"), self)
        action_settings.triggered.connect(self.rise_settings_window)

        menu_tools.addAction(action_settings)

        # Help
        # ----------------------------------------------------------------------
        menu_help = self.menu_bar.addMenu(_("&Help"))

    def rise_settings_window(self):
        if self.settings_window is None:
            self.settings_window = Settings_widget(self.palette, self.settings)
        self.settings_window.show()

    def move_to_center(self):
        frame = self.frameGeometry()
        frame.moveCenter(QtGui.QDesktopWidget().availableGeometry().center())
        self.move(frame.topLeft())