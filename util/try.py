#! python3
#coding: utf-8
import sys
sys.path.append('..')
from db.cn_db import Database
import PySide
from pprint import pprint
import pyqtgraph as pg
import pandas as pd
import numpy as np

if __name__ == '__main__':
    db = Database()
    symbol_list = ['600533']
    for tickerId in symbol_list:
        data = db.get_ticker_data_by_id_from_db(tickerId)
        close = np.array(data['close'])
        date = np.array(data['date'])

        close.shape = (close.shape[0],1)
        close = np.transpose(close)

        print(close,close.shape)
        
        # pw = pg.plot(close,pen='r')
        # win = pg.GraphicsWindow()
        pg.show(close)



