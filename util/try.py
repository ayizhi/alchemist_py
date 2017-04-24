#! python3
#coding: utf-8
import sys
sys.path.append('..')
from db.cn_db import Database
from pprint import pprint
import pyqtgraph as pg
import pandas as pd
import numpy as np
import pyqtgraph.examples

if __name__ == '__main__':
    db = Database()
    symbol_list = ['600533']
    for tickerId in symbol_list:
        data = db.get_ticker_data_by_id_from_db(tickerId)
        close = np.array(data['close'])
        date = np.array(data['date'])

        print(close,close.shape)

        pg.examples.run()

        data = np.random.normal(size=1000)
        pg.plot(close, title="Simplest possible plotting example")
        pg.QtGui.QApplication.exec_()
