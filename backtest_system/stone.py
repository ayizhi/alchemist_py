#coding: utf-8
#alchemist's stone

import datetime
import numpy as np
import pandas as pd

from backtest import Backtest
from data import HistoricalDbDataHandler
from event import SignalEvent
from execution import SimulatedExecutionHandler
from portfolio import Portfolio
from strategy import Strategy

class MovingAverageCrossStrategy(Strategy):
    def __init__(self,bars,events,short_window=100,long_window=100):
        self.bars = bars
        self.symbo_list = self.bars.symbo_list
        self.events = events
        self.short_window = short_window
        self.long_window = long_window

        self.bought = self._calculate_initial_bought()

    def _calculate_initial_bought(self):
        bought = {}
        for s in self.symbo_list:
            bought[s] = 'OUT'
        return bought


if __name__ = '__main__':
    symbo_list = ['600533','000503']
    initial_capital = 100000.0
    start_date = datetime.datetime(2015,1,1,0,0,0)
    heart_beat = 0.0

