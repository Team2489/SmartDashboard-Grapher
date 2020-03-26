from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtCore import Qt
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
from random import randint


import sys
import time
from networktables import NetworkTables
import numpy as np

# To see messages from networktables, you must setup logging
import logging

# logging.basicConfig(level=logging.DEBUG)

ip = "10.11.11.2"
NetworkTables.initialize(server=ip)


def valueChanged(table, key, value, isNew):
    print("valueChanged: key: '%s'; value: %s; isNew: %s" % (key, value, isNew))


def connectionListener(connected, info):
    print(info, "; Connected=%s" % connected)


NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

sd = NetworkTables.getTable("SmartDashboard")
# sd.addEntryListener(valueChanged)

def get():
    return (sd.getNumber("robotTime", -1))
def getspeed():
    return (sd.getNumber("speed", -1))
def getsetpoint():
    return (sd.getNumber("setpoint", -1))

class MainWindow(QtWidgets.QMainWindow):

    sigKeyPress = QtCore.pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        self.x = [get()]
        self.y = [getspeed()]
        self.y2 = [getsetpoint()]

        self.graphWidget.setBackground('w')
        # self.graphWidget.setXRange(0, 2000, padding=0)

        pen = pg.mkPen(color=(255, 0, 0), width=3)
        pen2 = pg.mkPen(color=(0, 0, 255), width=3)
        self.data_line =  self.graphWidget.plot(self.x, self.y, pen=pen)
        self.data_line2 =  self.graphWidget.plot(self.x, self.y2, pen=pen2)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):
        self.x.append(get())
        self.y.append(getspeed())
        self.y2.append(getsetpoint())

        # self.x = self.x[-100:]
        # self.y = self.y[-100:]

        self.data_line.setData(self.x, self.y)  # Update the data.
        self.data_line2.setData(self.x, self.y2)  # Update the data.
    
    def keyPressEvent(self, ev):
        # self.scene().keyPressEvent(ev)
        self.sigKeyPress.emit(ev)




app = pg.mkQApp()
w = MainWindow()
def keyPressed(evt):
    if evt.key() == Qt.Key_R:
        w.x = [0]
        w.y = [0]
        w.y2 = [1]
    elif evt.key() == Qt.Key_A:
        w.x = w.x[-10:]
        w.y = w.y[-10:]
        w.y2 = w.y2[-10:]
w.sigKeyPress.connect(keyPressed)
w.show()
sys.exit(app.exec_())