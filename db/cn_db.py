print '================== may the force be with you ================='
import pymongo
from pprint import pprint
from pymongo import MongoClient
import tushare


class Database():
	def __init__(self):
		self.client = MongoClient('localhost',27017);
		self.db = client.ticker_master

	def save_ticker_names_into_db():
		collection = db.symbol
		print 111