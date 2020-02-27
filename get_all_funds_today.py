# !/usr/bin/python
# -*- coding:utf-8 -*-

import db
import sys
import datetime
import urllib2
import re

def get_jingzhi(strfundcode, strdate):
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

	for line in tr_re.findall(json_fund_value):
		match = item_re.match(line)
		if match:
			entry = match.groups()
			print entry

	return entry



if __name__ == "__main__":	
	reload(sys)
	sys.setdefaultencoding('utf-8')
	

	strsdate = '2020-02-25'
	sdatetime = datetime.datetime.strptime(strsdate, '%Y-%m-%d')
	strsdate = datetime.datetime.strftime(sdatetime, '%Y-%m-%d')


	get_jingzhi('007817', strsdate)
	#main(sys.argv)