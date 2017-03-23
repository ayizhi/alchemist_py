#codeing: utf-8
import sys
sys.path.append(..)
from cn_db import Database

if __name__ == '__main__':
	Db = Database()
	Db.get_ticker_ids()