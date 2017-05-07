#coding: utf-8

import pandas as pd
import numpy as np
import sys
sys.path.append('..')

from abc import ABCMeta, abstractmethod

from db.cn_db import Database
from util.plot_util import PlotUtil
from event import MarketEvent




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
	def get_latest_bar_value(self,symbol,key_val):
		raise NotImplementedError("should implement get_latest_bar_value()")

	@abstractmethod
	def get_latest_bars_values(self,symbol,key_val,N=1):
		raise NotImplementedError("should implement get_latest_bars_values()")

	@abstractmethod
	def update_bars(self):
		raise NotImplementedError("should implement update_bars()")




class HistoricalDbDataHandler(DataHandler):

	def __init__(self,events,symbol_list):
		self.events = events
		self.symbol_list = symbol_list

		self.symbol_data = {}
		self.latest_symbol_data = {}
		self.bar_index = 0
		self.db = Database()
		self.continue_backtest = True

		self.get_symbol_data_init()

	def get_symbol_data_init(self):
		comb_index = None
		for s in self.symbol_list:
			self.symbol_data[s] = self.db.get_ticker_data_by_id_from_db(s)[['date','open','high','low','close','volume']].fillna(method='ffill').fillna(method="pad")

			if comb_index is None:
				comb_index = self.symbol_data[s].index
			else:
				comb_index.union(self.symbol_data[s].index)

			self.latest_symbol_data[s] = []

		#reindex the df with comb_index
		for s in self.symbol_list:
			self.symbol_data[s] = self.symbol_data[s].reindex(index=comb_index,method="pad").iterrows()

	def _get_new_bar(self,symbol):
		for d in self.symbol_data[symbol]:
			yield d

	def get_latest_bar(self,symbol):
		try:
			bars_list = self.latest_symbol_data[symbol]
		except KeyError:
			print("That symbol is not available in the historical data set.")
			raise
		else:
			return bars_list[-1]

	def get_latest_bars(self,symbol,N=1):
		try:
			bars_list = self.latest_symbol_data[symbol]
		except KeyError:
			print("That symbol is not available in the historical data set.")
			raise
		else:
			return bars_list[-N:]

	def get_latest_bar_datetime(self,symbol):
		try:
			bars_list = self.latest_symbol_data[symbol]
		except KeyError:
			print("That symbol is not available in the historical data set.")
			raise
		else:
			return bars_list[-1][0]

	def get_latest_bar_value(self,symbol,key_val):
		try:
			bars_list = self.latest_symbol_data[symbol]
		except KeyError:
			print("That symbol is not available in the historical data set.")
		else:
			return getattr(bars_list[-1][1],key_val)

	def get_latest_bars_values(self,symbol,key_val,N=1):
		try:
			bars_list = self.get_latest_bars(symbol,N)
		except KeyError:
			print("That symbol is not available in the historical data set.")
		else:
			return np.array([getattr(b[1],key_val) for b in bars_list])

	def update_bars(self):
		for s in self.symbol_list:
			try:
				bar = next(self._get_new_bar(s))
			except StopIteration:
				self.continue_backtest = False
			else:
				if bar is not None:
					self.latest_symbol_data[s].append(bar)
		self.events.put(MarketEvent())



