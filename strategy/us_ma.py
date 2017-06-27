#us moving average strategy
import sys
sys.path.append('..')
from db.us_db import US_Database
import numpy as np
import pandas as pd
import datetime
from strategy_base import Strategy

class MA_strategy(Strategy):
    def __init__(self):
        self.short_k = 5
        self.middle_k = 15
        self.long_k = 50
        self.target_range = 20 #计算周期


if __name__ == '__main__':
    db = US_Database()
    symbols = db.get_33_66_volume_by_day_symbol(10)
    for symbol in symbols:
        ticker = db.get_ticker_by_id(symbol,start_date=datetime.datetime(2017,1,1))
        print (ticker)
        break
