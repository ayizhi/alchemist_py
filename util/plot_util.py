#coding: utf-8
#数据工具库

import pandas as pd
import numpy as np
import pyqtgraph as pg
import pyqtgraph.examples
from pyqtgraph.Qt import QtGui


class PlotUtil(object):
    def __init__(self):
        self.win = pg.GraphicsWindow()
        self.win.resize(1000,600)

    def plot_line(self,np_normal):
        pg = self.win.addPlot(title="plot a line")
        pg.plot(np_normal,pen=(255,0,0))
        QtGui.QApplication.exec_()

    def plot_point(self,np_normal):
        pg = self.win.addPlot(title="plot points")
        pg.plot(np_normal,pen=(200,200,200), symbolBrush=(255,255,0), symbolPen='w')
        QtGui.QApplication.exec_()

    def plot_k(self,np_normal,np_short,np_middle,np_long,title):
        pg = self.win.addPlot(title="Multiple curves")
        pg.plot(np_normal, pen='w', name="normal")
        pg.plot(np_short, pen=(255,0,0), name="short")
        pg.plot(np_middle,pen=(0,255,0), name="middle")
        pg.plot(np_long,pen=(0,0,255),name="long")
        QtGui.QApplication.exec_()



# plt = PlotUtil()
# plt.plot()

# pyqtgraph.examples.run()