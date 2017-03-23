print '================== may the force be with you ================='
import pymongo
from pprint import pprint
from pymongo import MongoClient
import tushare as ts
import json
import pandas as pd
import numpy as np

class Database():
	def __init__(self):
		self.client = MongoClient('localhost',27017);
		self.db = self.client.ticker_master

	#存入，所有股票的name，与信息
	def save_ticker_names_into_db(self):
		collection = self.db.symbol
		ticker_list = ts.get_stock_basics()
		ticker_list['code'] = ticker_list.index
		ticker_json = json.loads(ticker_list.to_json(orient='records'))
		collection.insert(ticker_json)
	
	#获取 所有股票id，name，baseinfo
	def get_ticker_ids(self):
		collection = self.db.symbol
		return collection.find()


	#存入，根据股票id获取股票数据放入db
	def save_data_into_db_by_id(self,id):
		collection = self.db.daily_price
