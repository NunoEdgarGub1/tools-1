
import os, sys, time
from datetime import datetime
import random
import pylab as plt
import numpy as np
import h5py
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtGui, QtWidgets

class QPLZoomableGUI(QtWidgets.QMainWindow):

    def __init__(self, ui_panel):

        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.ui = ui_panel
        self.ui.setupUi(self)
         
        # connect to mouse events for zoom
        self.ui.canvas.mpl_connect('button_press_event', self.mouseClick)
        self.ui.canvas.mpl_connect('motion_notify_event', self.mouseMove)
        self.ui.canvas.mpl_connect('button_release_event', self.mouseRelease)
        self.mouse_clicked = False
        self.cursor_clicked = False

    def _update_figure (self):
        self.ui.canvas.update_figure()

    def _update_view(self):
        x0 = min (self.x0, self.x1)
        x1 = max (self.x0, self.x1)
        y0 = min (self.y0, self.y1)
        y1 = max (self.y0, self.y1)
        self.ui.canvas.set_range (axis1= [x0, x1], axis2 = [y0, y1])

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        print ("Close window...")
        ce.accept()

    def mouseClick(self, event):
        x = event.xdata
        if (x != None):
            self.cursor_clicked = self._is_click_near_cursor(x)
            if (self.cursor_clicked == False):
                self.x0 = event.xdata
                self.y0 = event.ydata
                self.mouse_clicked = True

    def mouseMove(self, event):
        pass

    def mouseRelease(self, event):
        if (event.xdata != None):
            x = event.xdata

            c = self.cursor_clicked
            if (c == False):
                self.x1 = x
                self.y1 = event.ydata
                if self.mouse_clicked:
                    self.mouse_clicked = False
                    self.set_range(self.x0, self.y0, self.x1, self.y1)
            else:
                self._set_cursor (cursor = c, position =x)

        self._update_view()

    def _set_cursor (self, cursor, position):
        self.ui.canvas.set_cursor (cursor=cursor, position=position)
        xA, xB = self.ui.canvas.get_cursors()
        self.ui.text_c0.setText (str(int(xA))+ " nm")
        self.ui.text_c1.setText (str(int(xB))+ " nm")
        self.ui.text_diff.setText (str(int(xB-xA))+ " nm")

    def _is_click_near_cursor (self, x):
        xA, xB = self.ui.canvas.get_cursors()
        vr = self.get_view_range()
        R = abs(vr[1]-vr[0])
        if (abs(x-xA)/R<0.02):
            a = "c0"
        elif (abs(x-xB)/R<0.02):
            a = "c1"
        else:
            a = False
        return a 

    def _slider_changed (self, event):
        D = self._view_range[1] - self._view_range[0]
        self.set_view_range (t0=event-D, t1=event)
        self._update_view()

    def set_range (self, x0, y0, x1, y1):
        t0 = x0
        t1 = x1

        try:
            if (t1>t0):
                if (t0<0):
                    t0 = 0
                if (t1>self._max_t):
                    t1 = self._max_t
                self._view_range = [t0, t1]
        except:
            pass

    def get_view_range (self):
        return self._view_range

    def _zoom_full (self):
        self.set_view_range (0, self._max_t)
        self._update_view()

    def _zoom_cursors (self):
        xA, xB = self.ui.canvas.get_cursors()
        self.set_view_range (xA*0.95, xB*1.05)
        self._update_view()

    def _zoom_funct (self, alpha):
        x0 = self._view_range[0]
        x1 = self._view_range[1]
        d0 = 0.5*(x0+x1)-alpha*(x1-x0)
        d1 = 0.5*(x0+x1)+alpha*(x1-x0)
        if (d0<0):
            d0 = 0
        if (d1>self._max_t):
            d1 = self._max_t
        return d0, d1

    def _zoom_out (self):
        d0, d1 = self._zoom_funct (alpha=1.)
        self.set_view_range (d0, d1)
        self._update_view()

    def _zoom_in (self):
        d0, d1 = self._zoom_funct (alpha=0.25)
        self.set_view_range (d0, d1)
        self._update()

