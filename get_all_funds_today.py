# !/usr/bin/python
# -*- coding:utf-8 -*-

import db
import sys
import datetime
import urllib2
import re

empty_entry = ('0000-00-00', '0.0000', '0.0000', '0.00%', '开放申购', '开放赎回')

# get a fund's informations
def get_fund_price(strfundcode, strdate):
	print 'fundcode', strfundcode
	try:
		url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=' + \
		      strfundcode + '&page=1&per=20&sdate=' + strdate + '&edate=' + strdate
		#print url + '\n'
		response = urllib2.urlopen(url)
	except urllib2.HTTPError, e:
		print e
		urllib_error_tag = True
	except StandardError, e:
		print e
		urllib_error_tag = True
	else:
		urllib_error_tag = False
	
	if urllib_error_tag == True:
		return '-1'

	# 当日所有基金
	json_fund_value = response.read().decode('utf-8')
	#print json_fund_value

	tr_re = re.compile(r'<tr>(.*?)</tr>')
	item_re = re.compile(r'''<td>(\d{4}-\d{2}-\d{2})</td><td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?></td>''', re.X)
	entry = ()
	for line in tr_re.findall(json_fund_value):
		match = item_re.match(line)
		if match:
			entry = match.groups()

	if len(entry) == 0:
		entry = empty_entry

	return entry

def getYesterday(): 
    yesterday = datetime.date.today() + datetime.timedelta(-1)
    strsdate = datetime.datetime.strftime(yesterday, '%Y-%m-%d')
    return strsdate

def convert_str(price):
	if price == '':
		return float(0.0)
	return float(price)


def main():
	yesterday = getYesterday()
	# get all fund code from db
	all_fundcodes = db.get_funds_list()

	# get al fund price informations
	l = []
	for fc in all_fundcodes:
		e = get_fund_price(fc, yesterday)
		print e
		t = (fc, yesterday, convert_str(e[1]), e[3], e[4], e[5], int(0))
		l.append(t)

	# save into db
	db.batch_insert(db.TABLE_FUNDSTODAY, l)

# 此脚本为了获取单日基金情况，执行的时间为第二天的凌晨3：00，所以使用昨天的时间
if __name__ == "__main__":	
	reload(sys)
	sys.setdefaultencoding('utf-8')
	
	main()







