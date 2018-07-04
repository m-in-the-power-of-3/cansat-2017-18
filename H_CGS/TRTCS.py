#!/usr/bin/python3
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore

from unpack import *

class First_screen(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(600, 300, 250, 100)
        self.setWindowTitle('TRTCS')
        self.button_log_reply = QtGui.QPushButton('LOG REPLY', self)
        self.button_log_reply.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button_log_reply.move(30, 20)
        self.connect(self.button_log_reply, QtCore.SIGNAL('clicked()'), self.button_log_reply_beh)
        self.button_enter = QtGui.QPushButton('Enter', self)
        self.button_enter.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button_enter.move(80, 60)
        self.connect(self.button_enter, QtCore.SIGNAL('clicked()'), self.close)
        self.button_telemetry = QtGui.QPushButton('TELEMETRY', self)
        self.button_telemetry.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button_telemetry.move(130, 20)
        self.connect(self.button_telemetry, QtCore.SIGNAL('clicked()'), self.button_telemetry_beh)
        #self.setFocus()
        #self.label = QtGui.QLineEdit(self)
        #self.label.move(130, 22)

    def button_log_reply_beh(self):
        print("Log reply")
        set_data_mode(False)

    def button_telemetry_beh(self):
        print("Telemetry")
        set_data_mode(True)

    def showDialog(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')
        if ok:
            self.label.setText(unicode(text))

if __name__ == "__main__":
    try:
        app = QtGui.QApplication(sys.argv)
        icon = First_screen()
        icon.show()

        pg.setConfigOptions(antialias=True)
        app.exec_()

        win = MainWindow()
        win.resize(1024, 768)
        win.show()

        data_generator = DataGenerator()
        data_generator.new_record.connect(win.on_new_record)
        data_generator.start()
        app.exec_()
        data_generator.close()
    except OSError:
        raise
    except BaseException:
        raise
        data_generator.close()
   