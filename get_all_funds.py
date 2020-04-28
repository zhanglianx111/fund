# !/usr/bin/python
# -*- coding:utf-8 -*-

import db

import urllib2
import json
import datetime
import logging

logger = logging.getLogger('main.get_all_funds')

def main():
	response_all_funds = urllib2.urlopen('http://fund.eastmoney.com/js/fundcode_search.js')
	all_funds_txt = response_all_funds.read()

	all_funds_txt = all_funds_txt[all_funds_txt.find('=')+2:all_funds_txt.rfind(';')]
	all_funds_list = json.loads(all_funds_txt.decode('utf-8'))

	flist = []
	for f in all_funds_list:
		tup = (f[0], f[1], f[2], f[3], f[4])
		flist.append(tup)

	# 存入数据库
	date_lastweek = datetime.datetime.strftime(datetime.date.today(), '%Y-%m-%d')
	old_count = db.get_list_count(db.TALBE_FUNDSLIST, date_lastweek)
	db.batch_insert(db.TALBE_FUNDSLIST, flist)
	new_count = len(flist)

	if new_count - old_count >= 0:
		logger.info('increase %s funds' % (new_count - old_count))
	else:
		logger.info('reduce %s funds' % (old_count - new_count))

if __name__ == "__main__":
	#today = datetime.datetime.strftime(datetime.date.today(), '%Y-%m-%d')
	main()