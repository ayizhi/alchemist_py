#看前十天的数据对后3天的盈利有什么影响
import sklearn
import pandas as pd
import numpy as np
from strategy_base import Strategy
import datetime

class Unicon_strategy(Strategy):
    def __init__(self):
        self.target_date = datetime.datetime(2017,3,1)
        self.feature_date_range = 10
        self.profit_date_range = 3