#!/usr/bin/env python
# -*- coding:utf-8 -*-


import requests
import json
import re
import db
from bs4 import BeautifulSoup


def get_singlepage_namenum(page):
	all_managers = [] 
 	url_page = 'http://fund.eastmoney.com/Data/FundDataPortfolio_Interface.aspx?dt=14&mc=returnjson&ft=all&pn=5000&pi='+str(page)+'&sc=abbname&st=asc'
	rawhtml = requests.get(url_page)
	listhtmltext = json.loads(rawhtml.text.replace("var returnjson=","").replace("data",'"data"').replace('record','"record"').replace('pages','"pages"').replace("curpage",'"curpage"'))  # 把字符串变成列表
	for i in range(len(listhtmltext['data'])):	
		manager = (listhtmltext['data'][i][0], \
			listhtmltext['data'][i][1], \
			listhtmltext['data'][i][2], \
			listhtmltext['data'][i][3], \
			listhtmltext['data'][i][4], \
			listhtmltext['data'][i][5])

		all_managers.append(manager)
		
	db.batch_insert_managers(all_managers)

 
def get_pages_number():
	url_page0 = 'http://fund.eastmoney.com/Data/FundDataPortfolio_Interface.aspx?dt=14&mc=returnjson&ft=all&pn=5000&pi=0&sc=abbname&st=asc'
	rawhtml = requests.get(url_page0)
	listhtmltext = json.loads(rawhtml.text.replace("var returnjson=","").replace("data",'"data"').replace('record','"record"').replace('pages','"pages"').replace("curpage",'"curpage"'))  # 把字符串变成列表
	pages = listhtmltext['pages']
	return pages


def update_managers():
	pages = get_pages_number()
	for i in range(pages):
		get_singlepage_namenum(i + 1)


if __name__ == '__main__':
	funds = db.get_managers_funds()
	for f in funds:
		for ff in f:
			fff = ff.split(',')
			for f4 in fff:
				print f4
