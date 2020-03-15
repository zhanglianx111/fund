# !/usr/bin/python
# -*- coding:utf-8 -*-

import urllib2
import logging
from bs4 import BeautifulSoup
import bs4

#logger = logging.getLogger('main.get_fund_company')

def get_fund_companies():
	url = "http://fund.eastmoney.com/Company/home/gspmlist?fundType=0"
	try:
		response = urllib2.urlopen(url, timeout=10)

	except urllib2.HTTPError, e:
		print e
		#logger.error(e)


	# 所有基金公司
	fund_companies = response.read().decode('utf-8')


	root = BeautifulSoup(fund_companies,                #HTML文档字符串
                         'html.parser',                  #HTML解析器
                         from_encoding = 'utf-8'         #HTML文档编码 
                        )
	companies_tmp = []
	companies = []
	trs = root.find_all('tr')
	for tr in trs:
		company = []
		tds = tr.find_all("td")
		for i in range(len(tds)):
			#print tds[i].get_text()
			company.append(tds[i].get_text())

		companies_tmp.append(company)
		
	for c in companies_tmp:
		if len(c) == 8:
			#print c[1], str.split(c[3].encode("utf-8"))[0], str.split(c[5].encode("utf-8"))[0], c[6], c[7]
			companies.append((c[1], str.split(c[3].encode("utf-8"))[0], str.split(c[5].encode("utf-8"))[0], c[6], c[7]))
	return companies
	
if __name__ == '__main__':
	cs = get_fund_companies()
	for c in cs:
		print c
		print '-------------'