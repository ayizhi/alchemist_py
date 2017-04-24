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
        y = np.random.normal(size=close.shape[0])

        # close.shape = (close.shape[0],1)
        # close = np.transpose(close)

        print(close,close.shape)
        
        # pw = pg.plot(close,pen='r')
        # win = pg.GraphicsWindow()

        # image = pg.plot(close, y, pen=None, symbol='o')
        # pg.image(close) 

        # import pyqtgraph.examples
        # pyqtgraph.examples.run()    
        # 


        pg.examples.run()

        data = np.random.normal(size=1000)
        pg.plot(close, title="Simplest possible plotting example")
        pg.QtGui.QApplication.exec_()


        ## Start Qt event loop unless running in interactive mode or using pyside.
        # if __name__ == '__main__':
        #     import sys
        #     if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        #         pg.QtGui.QApplication.exec_()