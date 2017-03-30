#coding: utf-8
import datetime
import sys
sys.path.append('..')
from cn_db import Database
from pprint import pprint

if __name__ == '__main__':
	Db = Database()
	Db.get_middle_33_volume_from_db(20,'2017-03-24')