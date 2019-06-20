#!/usr/bin/python3
from sourse.sourse import *

if __name__ == "__main__":
    application = QtGui.QApplication([])
    win = Main_window()#theme.set_colour_theme(COLOUR_THEME))
    #update_settings("/home/developer/git/cansat-2017-2018/GCS/config.py")
    win.show()
    exit(application.exec_())
    app.exit()
