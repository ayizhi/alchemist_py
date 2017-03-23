print '================== may the force be with you ================='
import pymongo
from pprint import pprint
from pymongo import MongoClient
import tushare as ts
import json

class Database():
	def __init__(self):
		self.client = MongoClient('localhost',27017);
		self.db = self.client.ticker_master

	def save_ticker_names_into_db(self):
		collection = self.db.symbol
		ticker_list = ts.get_stock_basics()
		ticker_json = json.loads(ticker_list.to_json(orient='records'))
		collection.insert(ticker_json)