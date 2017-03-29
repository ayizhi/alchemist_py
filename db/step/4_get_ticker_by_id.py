#coding: utf-8
import datetime
import sys
sys.path.append('..')
from cn_db import Database
from pprint import pprint

if __name__ == "__main__":
	Db = Database()
	ticker_ids = Db.get_ticker_ids_from_db()
	i = 0
	for ticker in ticker_ids:
		i = i + 1
		ticker_id = ticker['code']
		ticker_name = ticker['name']
		print ticker_id,ticker_name,'==='
		ticker_data = Db.get_ticker_data_by_id_from_db(ticker_id)
		for item in ticker_data:
			print item
			print '-------'
		print '================='
		print '================='
		print '================='
		if i > 100:
			break