#test the strategy
import pandas as pd
import numpy as np
import sys
sys.path.append('../')
from db.us_db import US_Database
import datetime

class Test_util(object):
    def __init__(self):
        self.db = US_Database()

    def test_profit_by_date(self,ticker,date):
        target_date_60 = date + datetime.timedelta(days=60)
        profit_60 = self.db.get_profit_by_days(ticker,59,target_date_60)
        profit_60_max = self.db.get_max_profit_by_days(ticker,59,target_date_60)

        target_date_20 = date + datetime.timedelta(days=20)
        profit_20 = self.db.get_profit_by_days(ticker,19,target_date_20)
        profit_20_max = self.db.get_max_profit_by_days(ticker,19,target_date_20)

        target_date_10 = date + datetime.timedelta(days=10)
        profit_10 = self.db.get_profit_by_days(ticker,9,target_date_10)
        profit_10_max = self.db.get_max_profit_by_days(ticker,9,target_date_10)

        target_date_6 = date + datetime.timedelta(days=6)
        profit_6 = self.db.get_profit_by_days(ticker,5,target_date_6)
        profit_6_max = self.db.get_max_profit_by_days(ticker,5,target_date_6)

        target_date_3 = date + datetime.timedelta(days=3)
        profit_3 = self.db.get_profit_by_days(ticker,2,target_date_3)
        profit_3_max = self.db.get_max_profit_by_days(ticker,2,target_date_3)


        return {
                'ticker': ticker,
                'profit_60': profit_60,
                'profit_60_max': profit_60_max,
                'profit_20': profit_20,
                'profit_20_max': profit_20_max,
                'profit_10': profit_10,
                'profit_10_max': profit_10_max,
                'profit_6': profit_6,
                'profit_6_max': profit_6_max,
                'profit_3': profit_3,
                'profit_3_max': profit_3_max,
                }

