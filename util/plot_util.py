#coding: utf-8
#数据工具库

import pandas as pd
import numpy as np
import pyqtgraph as pg
import pyqtgraph.examples


class PlotUtil(object):
    def __init__(self):
        self.win = pg.GraphicsWindow()
        self.win.resize(1000,600)


    def plot(plot_list):

        p2 = win.addPlot(title="Multiple curves")
        p2.plot(np.random.normal(size=100), pen=(255,0,0), name="Red curve")
        p2.plot(np.random.normal(size=110)+5, pen=(0,255,0), name="Green curve")
        p2.plot(np.random.normal(size=120)+10, pen=(0,0,255), name="Blue curve")
