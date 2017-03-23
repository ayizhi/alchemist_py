#coding: utf-8
import sys
sys.path.append('..')
from cn_db import Database

if __name__ == '__main__' :
    Db = Database();
    Db.save_ticker_names_into_db()