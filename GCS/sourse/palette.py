from PyQt5 import QtGui
import random

default = QtGui.QPalette()

dark = QtGui.QPalette()
dark.setColor(QtGui.QPalette.Window, QtGui.QColor(30, 30, 30, 255))
dark.setColor(QtGui.QPalette.WindowText, QtGui.QColor(255, 255, 255, 255))
dark.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(255, 255, 255, 255))
dark.setColor(QtGui.QPalette.Button, QtGui.QColor(80, 80, 80, 255))
dark.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(255, 255, 255, 255))

random_ct = QtGui.QPalette()
random_ct.setColor(QtGui.QPalette.Window, QtGui.QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
random_ct.setColor(QtGui.QPalette.WindowText, QtGui.QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
random_ct.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
random_ct.setColor(QtGui.QPalette.Button, QtGui.QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
random_ct.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

palette_list = {'default': default,
                'dark': dark,
                'random_ct': random_ct}