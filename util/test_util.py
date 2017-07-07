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
        target_date_10 = date + datetime.timedelta(days=10)
        profit_10,profit_10_percent = self.db.get_profit_by_days(ticker,9,target_date_10)
        profit_10_max,profit_10_max_percent = self.db.get_max_profit_by_days(ticker,9,target_date_10)

        target_date_6 = date + datetime.timedelta(days=6)
        profit_6,profit_6_percent = self.db.get_profit_by_days(ticker,5,target_date_6)
        profit_6_max,profit_6_max_percent = self.db.get_max_profit_by_days(ticker,5,target_date_6)

        target_date_4 = date + datetime.timedelta(days=4)
        profit_4,profit_4_percent = self.db.get_profit_by_days(ticker,4,target_date_4)
        profit_4_max,profit_4_max_percent = self.db.get_max_profit_by_days(ticker,4,target_date_4)

        std_10 = self.db.get_std_by_days(ticker,10,date)

        return {
                'ticker': ticker,
                'std_10': std_10,
                'profit_10': profit_10_percent,
                'profit_10_max': profit_10_max_percent,
                'profit_6': profit_6_percent,
                'profit_6_max': profit_6_max_percent,
                'profit_4': profit_4_percent,
                'profit_4_max': profit_4_max_percent,
                }

