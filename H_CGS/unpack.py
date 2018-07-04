import struct
from itertools import chain
from enum import IntEnum
from math import acos

import numpy as np
from stl import mesh
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph import Qt
import pyqtgraph as pg
import pyqtgraph.opengl as gl

from hermes_ts import *

MESH_PATH = './theplane.stl'

data_mode = True


class Record(QtCore.QObject):
    class SensorKey(IntEnum):
        ACC_X = 0
        ACC_Y = 1
        ACC_Z = 2
        GYRO_X = 3
        GYRO_Y = 4
        GYRO_Z = 5
        LUX = 6
        VOL_1 = 7
        VOL_2 = 8
        VOL_3 = 9
        VOL_4 = 10

    def __init__(self, block):
        super(Record, self).__init__()

        self.sensors_data = block[1:]

        self.start_time = block[0]


class PlaneWidget(gl.GLViewWidget):
    def __init__(self, mesh_path, *args, **kwargs):
        super(PlaneWidget, self).__init__(*args, **kwargs)
        self.setCameraPosition(distance=40)

        g = gl.GLGridItem()
        g.scale(2, 2, 1)
        g.translate(0, 0, -2)
        self.addItem(g)

        self.plane_axis = gl.GLAxisItem()
        self.plane_axis.setSize(x=500, y=500, z=500)
        self.addItem(self.plane_axis)

        verts = self._get_mesh_points(mesh_path)
        faces = np.array([(i, i + 1, i + 2,) for i in range(0, len(verts), 3)])
        colors = np.array([(0.0, 1.0, 0.0, 1.0,) for i in range(0, len(verts), 3)])
        self.mesh = gl.GLMeshItem(vertexes=verts, faces=faces, faceColors=colors, smooth=False, shader='shaded')
        self.addItem(self.mesh)
        self._update_mesh([0, 0, -1])


    def on_new_records(self, records):
        record = records[-1]
        acc_v = [
            record.sensors_data[Record.SensorKey.ACC_X],
            record.sensors_data[Record.SensorKey.ACC_Y],
            record.sensors_data[Record.SensorKey.ACC_Z],
        ]

        self._update_mesh(acc_v)


    def _get_mesh_points(self, mesh_path):
        your_mesh = mesh.Mesh.from_file(mesh_path)
        points = your_mesh.points

        points = np.array(list(chain(*points)))
        i = 0
        nd_points = np.ndarray(shape=(len(points)//3, 3,))
        for i in range(0, len(points)//3):
            nd_points[i] = points[i*3: (i+1)*3]

        return nd_points

    def _update_mesh(self, nadir_v):

        nadir_v_original = np.array([0, 0, 1], dtype='double')
        nadir_v_original /= np.linalg.norm(nadir_v_original)

        nadir_v = np.array(nadir_v, dtype='double')
        nadir_v /= np.linalg.norm(nadir_v)

        angle = np.dot(nadir_v_original, nadir_v)
        angle = acos(angle)
        angle = angle * 180 / np.pi
        axis = np.cross(nadir_v_original, nadir_v)

        # print(axis, angle)


        def do_things(target, move=True):
            target.resetTransform()
            target.scale(1 / 50, 1 / 50, 1 / 50)
            target.rotate(90, 1, 0, 0)
            target.rotate(180, 0, 0, 1)
            if move: target.translate(0, -3, 0)
            target.rotate(angle, axis[0], axis[1], axis[2])

        do_things(self.mesh)
        do_things(self.plane_axis, move=False)


class PlotWidget(pg.GraphicsLayoutWidget):
    acc_pens = ['r', 'g', 'b']
    gyro_pens = ['r', 'g', 'b']
    vol_pens = ['r', 'g', 'b']
    lux_pens = ['r', 'g', 'b', 'w']

    class CurveContainer:
        buffer_size = 10000

        def __init__(self, plot, pen, data_extractor):
            self.plot = plot
            self.pen = pen
            self.data_extractor = data_extractor

            self.curve = None
            self.x_data = []
            self.y_data = []

        def consume_records(self, records):
            self.x_data += [record.start_time for record in records]
            self.y_data += [self.data_extractor(record) for record in records]

            if len(self.x_data) > self.buffer_size:
                self.x_data, self.y_data = self.x_data[-self.buffer_size: ], self.y_data[-self.buffer_size: ]

            if self.curve is None:
                self.curve = self.plot.plot(x=self.x_data, y=self.y_data, pen=self.pen)
            else:
                self.curve.setData(x=self.x_data, y=self.y_data)


    def __init__(self, *args, **kwargs):
        super(PlotWidget, self).__init__(*args, **kwargs)
        axis_x_acc = pg.AxisItem(orientation='left')
        axis_x_acc.setLabel("Accel")

        axis_y_acc = pg.AxisItem(orientation='bottom')
        axis_y_acc.setLabel("time")

        axis_x_gyro = pg.AxisItem(orientation='left')
        axis_x_gyro.setLabel("Gyro")

        axis_y_gyro = pg.AxisItem(orientation='bottom')
        axis_y_gyro.setLabel("time")

        axis_x_lux = pg.AxisItem(orientation='left')
        axis_x_lux.setLabel("Lux")

        axis_y_lux = pg.AxisItem(orientation='bottom')
        axis_y_lux.setLabel("time")

        axis_x_vol_1 = pg.AxisItem(orientation='left')
        axis_x_vol_1.setLabel("Voltage 1")

        axis_y_vol_1 = pg.AxisItem(orientation='bottom')
        axis_y_vol_1.setLabel("time")

        axis_x_vol_2 = pg.AxisItem(orientation='left')
        axis_x_vol_2.setLabel("Voltage 1")

        axis_y_vol_2 = pg.AxisItem(orientation='bottom')
        axis_y_vol_2.setLabel("time")

        axis_x_vol_3 = pg.AxisItem(orientation='left')
        axis_x_vol_3.setLabel("Voltage 1")

        axis_y_vol_3 = pg.AxisItem(orientation='bottom')
        axis_y_vol_3.setLabel("time")

        axis_x_vol_4 = pg.AxisItem(orientation='left')
        axis_x_vol_4.setLabel("Voltage 1")

        axis_y_vol_4 = pg.AxisItem(orientation='bottom')
        axis_y_vol_4.setLabel("time")

        self.p_acc = self.addPlot(row=0, col=1, axisItems={'left': axis_x_acc, 'bottom': axis_y_acc})
        self.p_gyro = self.addPlot(row=1, col=1, axisItems={'left': axis_x_gyro, 'bottom': axis_y_gyro})
        self.p_lux = self.addPlot(row=2, col=1, axisItems={'left': axis_x_lux, 'bottom': axis_y_lux})
        self.p_vol_1 = self.addPlot(row=0, col=0, axisItems={'left': axis_x_vol_1, 'bottom': axis_y_vol_1})
        self.p_vol_2 = self.addPlot(row=1, col=0, axisItems={'left': axis_x_vol_2, 'bottom': axis_y_vol_2})
        self.p_vol_3 = self.addPlot(row=2, col=0, axisItems={'left': axis_x_vol_3, 'bottom': axis_y_vol_3})
        self.p_vol_4 = self.addPlot(row=3, col=0, axisItems={'left': axis_x_vol_4, 'bottom': axis_y_vol_4})

        acc_converter = lambda value: value# * 0.061 * (16 >> 1) / 1000.0
        gyro_converter = lambda value: value
        vol_1_converter = lambda value: value
        vol_2_converter = lambda value: value
        vol_3_converter = lambda value: value
        vol_4_converter = lambda value: value
        lux_converter = lambda value: value

        skey = Record.SensorKey


        self.acc_curves = [
            self.CurveContainer(self.p_acc, self.acc_pens[0], lambda record: acc_converter(record.sensors_data[skey.ACC_X])),
            self.CurveContainer(self.p_acc, self.acc_pens[1], lambda record: acc_converter(record.sensors_data[skey.ACC_Y])),
            self.CurveContainer(self.p_acc, self.acc_pens[2], lambda record: acc_converter(record.sensors_data[skey.ACC_Z])),
        ]

        self.gyro_curves = [
            self.CurveContainer(self.p_gyro, self.gyro_pens[0], lambda record: gyro_converter(record.sensors_data[skey.GYRO_X])),
            self.CurveContainer(self.p_gyro, self.gyro_pens[1], lambda record: gyro_converter(record.sensors_data[skey.GYRO_Y])),
            self.CurveContainer(self.p_gyro, self.gyro_pens[2], lambda record: gyro_converter(record.sensors_data[skey.GYRO_Z])),
        ]

        self.lux_curves = [
            self.CurveContainer(self.p_lux, self.lux_pens[0], lambda record: lux_converter(record.sensors_data[skey.LUX])),
        ]

        self.vol_curves_1 = [
            self.CurveContainer(self.p_vol_1, self.vol_pens[0], lambda record: vol_1_converter(record.sensors_data[skey.VOL_1])),
        ]

        self.vol_curves_2 = [
            self.CurveContainer(self.p_vol_2, self.vol_pens[0], lambda record: vol_2_converter(record.sensors_data[skey.VOL_2])),
        ]

        self.vol_curves_3 = [
            self.CurveContainer(self.p_vol_3, self.vol_pens[0], lambda record: vol_3_converter(record.sensors_data[skey.VOL_3])),
        ]

        self.vol_curves_4 = [
            self.CurveContainer(self.p_vol_4, self.vol_pens[0], lambda record: vol_4_converter(record.sensors_data[skey.VOL_4])),
        ]

    def on_new_records(self, records):
        for curve in chain(self.acc_curves, self.gyro_curves, self.lux_curves,
                           self.vol_curves_1, self.vol_curves_2,
                           self.vol_curves_3, self.vol_curves_4):
            curve.consume_records(records)



class MainWindow(QtGui.QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        layout = QtGui.QHBoxLayout(self)
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Background, QtGui.QColor(0));
        self.setAutoFillBackground(True);
        self.setPalette(pal);

        self.plot_widget = PlotWidget(parent=self)
        self.plane_widget = PlaneWidget(mesh_path=MESH_PATH, parent=self)
        layout.addWidget(self.plot_widget, stretch=18)
        layout.addWidget(self.plane_widget, stretch=12)

    @QtCore.pyqtSlot(list)
    def on_new_record(self, records):
        self.plane_widget.on_new_records(records)
        self.plot_widget.on_new_records(records)


class DataGenerator(QtCore.QThread):
    new_record = QtCore.pyqtSignal(list)

    def __init__(self, *args, **kwargs):
        super(DataGenerator, self).__init__(*args, **kwargs)
        self.data_obj = Data(data_mode)

    def run(self):
        global data_mode
        
        records = []
        while True:
            time.sleep(0.05)
            block = self.data_obj.read_data()
            records.append(Record(block))
            print(records[-1].sensors_data)
            if len(records) > 50:
                self.new_record.emit(records)
                records = []


    def close(self):
        self.data_obj.stop()


class Data():
    def __init__(self, mode_=False):
        self.mode = mode_
        if not self.mode:
            self.data = H_log()
        else:
            self.data = H_telemetry()
            self.data.setup_socket()
            self.data.setup()

    def read_data(self):
        if not self.mode:
            return self.data.read_log()
        else:
            return self.data.read_telemetry()

    def stop(self):
        if (self.mode):
            self.data.close()
    

def set_data_mode(mode):
    global data_mode
    data_mode = mode


if __name__ == "__main__":
    try:
        app = QtGui.QApplication([])
        pg.setConfigOptions(antialias=True)

        win = MainWindow()
        win.resize(1024, 768)
        win.show()

        data_generator = DataGenerator()
        data_generator.new_record.connect(win.on_new_record)
        data_generator.start()
    except Exception:
        data_generator.close()

    exit(app.exec_())
