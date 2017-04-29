#coding: utf-8
print ('================== may the force be with you =================')
import pymongo
from pprint import pprint
from pymongo import MongoClient
import tushare as ts
import json
import pandas as pd
import numpy as np
import datetime

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

	#存入，根据股票id获取股票数据放入db
	def save_data_into_db_by_id(self,ticker_id):
		collection = self.db.daily_price
		f = open('error.txt','w')

		try:
			ticker_data = ts.get_k_data(ticker_id);
			print (ticker_data,'==============================')
			now = datetime.date.today()
			ticker_data['update_date'] = str(now)
			ticker_json = json.loads(ticker_data.to_json(orient="records"))
			collection.insert(ticker_json)
			print ('insert success ===========================')
		except:#如果获取失败
			f.truncate()
			f.write(ticker_id)
		f.close()

	#存入，从数据库里的最后一天到今天
	def save_data_into_db_by_id_until_today(self,ticker_id):
		collection = self.db.daily_price
		f = open('error.txt','w')
		try:
			ticker_list = collection.find({'code': ticker_id}).sort('date',pymongo.DESCENDING)
			last_date = ticker_list[0]['date']
			#往后算一天
			begin_date = datetime.datetime.strptime(last_date,'%Y-%m-%d') + datetime.timedelta(days = 1)
			today = datetime.date.today()
			#都转为str
			begin_date = begin_date.strftime("%Y-%m-%d")
			today = today.strftime("%Y-%m-%d")
			print ('===========',begin_date,'=====',today,'============')
			ticker_data = ts.get_k_data(ticker_id,start=begin_date,end=today,retry_count=10)
			print (ticker_data)
			ticker_json = json.loads(ticker_data.to_json(orient="records"))
			collection.insert(ticker_json)
			print ('insert success ===========================')
		except:
			print ('data has problem')
			f.write(ticker_id)
			f.write(',\\')
		f.close()


	#获取 所有股票id，name，baseinfo
	def get_ticker_ids_from_db(self):
		collection = self.db.symbol
		return pd.DataFrame(list(collection.find()))

	#读取一只股票的所有信息
	def get_ticker_data_by_id_from_db(self,ticker_id,start='',end=datetime.date.today()):
		collection = self.db.daily_price
		if type(end) == datetime.datetime or type(end) == datetime.date :
			end = end.strftime('%Y-%m-%d')


		try:
			date_range = {'$lt': end}
			if start != '':
				date_range['$gte'] = start
			ticker_data = collection.find({'code': ticker_id,'date':date_range})
			ticker_data = pd.DataFrame(list(ticker_data))
			return ticker_data
		except:
			print ('get data by id has error')
			f = open('error.txt','w')
			f.write(ticker_id)
			f.write(',\\')
			f.close()

	#获取一只股票的average volume
	def get_average_volume_by_id(self,ticker_id,day_range,markDate=datetime.date.today()):
		collection = self.db.daily_price
		#可传字符串，可传datetime对象
		if type(markDate) == datetime.datetime or type(markDate) == datetime.date :
			startDate = markDate + datetime.timedelta(days = -1 * day_range)
			endDate = markDate.strftime('%Y-%m-%d')
		elif type(markDate) == str:
			startDate = datetime.datetime.strptime(markDate,'%Y-%m-%d') + datetime.timedelta(days = -1 * day_range)
			endDate = markDate


		try:

			day_range_condition = {'$gte': str(startDate), '$lt': str(endDate)}
			ticker_data = collection.find({'code': ticker_id,'date': day_range_condition})
			ticker_df = pd.DataFrame(list(ticker_data))
			return ticker_df['volume'].mean()

		except:
			f = open('error.txt','w')
			f.write(ticker_id)
			f.write(',\\')
			f.close()

