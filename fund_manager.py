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


'''
def get_totalinfo():
	#开始二次爬虫。
	for unitnamenum in get_singlepage_namenum(page):
		print unitnamenum
		res = requests.get('http://fund.eastmoney.com/manager/{unitnamenum}.html')			
		res.encoding = ('utf8') #解决乱码
		#text=res.text.encode('ISO-8859-1').decode('gb18030') #另一种解决乱码的方式
		soupunit = BeautifulSoup(res.text,"lxml")
		name=[]	
		fund=[]
		for unitfund in soupunit.find_all("tbody")[1].find_all("tr"):
			name.extend((listhtmltext)['data'][i][1]) #managername 
			for unitfund_info in unitfund.find_all("td")[0]:
				fund.extend(unitfund_info.text.replace("\n","").replace("\t","")) #fundcode
		info=[]
		for i in range(0,len(fund)):
			info.append(list(name[i],fund[i])) #managername 
		return info
 '''
def update_managers():
	pages = get_pages_number()
	for i in range(pages):
		get_singlepage_namenum(i + 1)