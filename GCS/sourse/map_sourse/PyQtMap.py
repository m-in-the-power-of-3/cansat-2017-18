doTrace = False

import json
import os

import decorator

from PyQt5.QtCore import pyqtSignal, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtNetwork import QNetworkDiskCache
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebPage, QWebView
from PyQt5.QtWidgets import QApplication

class Open_street_map(QWebView):
    mapMoved = pyqtSignal(float, float)
    mapClicked = pyqtSignal(float, float)
    mapRightClicked = pyqtSignal(float, float)
    mapDoubleClicked = pyqtSignal(float, float)

    markerMoved = pyqtSignal(str, float, float)
    markerClicked = pyqtSignal(str, float, float)
    markerDoubleClicked = pyqtSignal(str, float, float)
    markerRightClicked = pyqtSignal(str, float, float)

    def __init__(self):
        super(Open_street_map, self).__init__()

        cache = QNetworkDiskCache()
        cache.setCacheDirectory("cache")
        self.page().networkAccessManager().setCache(cache)
        self.page().networkAccessManager()

        self.initialized = False

        basePath = os.path.abspath(os.path.dirname(__file__))
        url = 'file://' + basePath + '/map.html'
        self.load(QUrl(url))

        self.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)

        self.loadFinished.connect(self.onLoadFinished)
        self.linkClicked.connect(QDesktopServices.openUrl)

    def onLoadFinished(self, ok):
        if self.initialized:
            return

        self.initialized = True
        self.centerAt(0, 0)
        self.setZoom(10)

    def waitUntilReady(self):
        while not self.initialized:
            QApplication.processEvents()

    def runScript(self, script):
        return self.page().mainFrame().evaluateJavaScript(script)

    def centerAt(self, latitude, longitude):
        self.runScript("set_center({}, {})".format(latitude, longitude))

    def setZoom(self, zoom):
        self.runScript("set_zoom({})".format(zoom))

    def center(self):
        center = self.runScript("get_center()")
        return center['lat'], center['lng']

    def addMarker(self, key, latitude, longitude, **extra):
        return self.runScript("add_marker(key={!r},"
                              "latitude= {}, "
                              "longitude= {}, {});".format(key, latitude, longitude, json.dumps(extra)))

    def moveMarker(self, key, latitude, longitude):
        self.runScript("move_marker(key={!r},"
                       "latitude= {}, "
                       "longitude= {});".format(key, latitude, longitude))

    def positionMarker(self, key):
        return tuple(self.runScript("pos_marker(key={!r});".format(key)))
