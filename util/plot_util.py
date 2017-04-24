#coding: urf-8
#数据工具库

import pandas as pd
import numpy as np
import pyqtgraph as pg
import pyqtgraph.examples


class PlotUtil(object):
    def __init__(self):
        self.win = pg.GraphicsWindow()
        self.win.resize(1000,600)