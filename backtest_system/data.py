#coding: utf-8

import pandas as pd
import numpy as np
import sys
sys.path.append('..')

from abc import ABCMeta, abstractmethod

from db.cn_db import Database
from util.db_util import DbUtil
from util.plot_util import PlotUtil




class DataHandler(object):
	__metaclass__ = ABCMeta

	@abstractmethod
	def get_latest_bar(self,symbol):
		raise NotImplementedError("should implement get_latest_bar()")

	@abstractmethod
	def get_latest_bars(self,symbol,N=1):
		raise NotImplementedError("should implement get_latest_bars()")

	@abstractmethod
	def get_latest_bar_datetime(self,symbol):
		raise NotImplementedError("should implement get_latest_bar_datetime()")

	@abstractmethod
	def get_latest_bar_value(self,symbol,val_type):
		raise NotImplementedError("should implement get_latest_bar_value()")

	@abstractmethod
	def get_latest_bars_values(self,symbol,val_type,N=1):
		raise NotImplementedError("should implement get_latest_bars_values()")

	@abstractmethod
	def update_bars(self):
		raise NotImplementedError("should implement update_bars()")




class DBHandler(DataHandler):

	def __init__(self,events,symbol_list):
		self.symbol_list = symbol_list

		self.symbol_data = {}
		self.latest_symbol_data = {}
		self.continue_backtest = True
		self.bar_index = 0
		self.db = Database()

	def get_symbol_data(self):
		comb_index = None
		for symbol_id in self.symbol_list:
			self.symbol_data[symbol_id] = db.get_ticker_data_by_id_from_db(symbol_id)[['date','open','high','low','close','volume']]

			if comb_index is None:
				comb_index = self.symbol_data[symbol_id].index
			else:
				comb_index.union(self.symbol_data[symbol_id].index)

			self.latest_symbol_data[symbol_id] = []

		#reindex the df with comb_index
		for symbol_id in self.symbol_list:
			self.symbol_data[symbol_id] = self.symbol_data[symbol_id].reindex(index=comb_index,method="pad").iterrows()



db = Database()

symbol_list = ['600533','603050']
dbhandler = DBHandler('daily_price',symbol_list)
dbhandler.get_symbol_data()

