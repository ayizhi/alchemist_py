#coding: utf-8
import datetime
import sys
sys.path.append('..')
from cn_db import Database
from pprint import pprint

if __name__ == '__main__':
	Db = Database()
	ticker_ids = Db.get_ticker_ids_from_db()
	i = 0
	for ticker in ticker_ids:
		i = i + 1

		ticker_id = ticker['code']
		ticker_name = ticker['name']
		print ticker_id,ticker_name
		Db.get_average_volume_by_id(ticker_id,15)
		if i > 100 :
			break