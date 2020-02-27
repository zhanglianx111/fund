# !/usr/bin/python
# -*- coding:utf-8 -*-
import db
import urllib2
import json
import sys

def main():
	response_all_funds = urllib2.urlopen('http://fund.eastmoney.com/js/fundcode_search.js')
	all_funds_txt = response_all_funds.read()

	#print all_funds_txt

	all_funds_txt = all_funds_txt[all_funds_txt.find('=')+2:all_funds_txt.rfind(';')]
	all_funds_list = json.loads(all_funds_txt.decode('utf-8'))

	list = []
	for f in all_funds_list:
		tup = (f[0], f[1], f[2], f[3], f[4])
		list.append(tup)

	# 存入数据库
	db.batch_insert(db.TALBE_FUNDSLIST, list)

if __name__ == "__main__":
	main()