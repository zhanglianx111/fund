# !/usr/bin/python
# -*- coding:utf-8 -*-

import db
import mail

import sys
import datetime
import urllib2
import re
import logging
import threading
import time

logger = logging.getLogger('main.get_all_funds_today')

empty_entry = ('0000-00-00', '0.0000', '0.0000', '0.00%', '开放申购', '开放赎回')

# 每个线程获取500基金情况
NUMBER_PER_THREADING = 500
SLEEP_TIME = 0.01
TIMEOUT = 120
DOMAIN ='fund.eastmoney.com'



class MyThread(threading.Thread):
	def __init__(self, func, args = ()):
		super(MyThread, self).__init__()
		self.func = func
		self.args = args
		self.result = []

	def run(self):
		self.result = self.func(*self.args)

	def get_result(self):
		try:
			return self.result
		except Exception as err:
			logger.error(err)
			return err


# get a fund's informations
def get_fund_price(strfundcode, strdate):
	try:
		url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=' + \
		      strfundcode + '&page=1&per=1&sdate=' + strdate + '&edate=' + strdate
		response = urllib2.urlopen(url, timeout=TIMEOUT)
	except urllib2.HTTPError, e:
		logger.error(e)
		urllib_error_tag = True
	except StandardError, e:
		logger.error(e)
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

	if entry[3] == '':
		entry = entry[:3] + ('0.00%',) + entry[4:]
	return entry

def getYesterday(): 
	yesterday = datetime.date.today() + datetime.timedelta(-1)
	strsdate = datetime.datetime.strftime(yesterday, '%Y-%m-%d')
	return strsdate

def convert_str(price):
	if price == '':
		return float(0.0)
	return float(price)


def fetch(sub_funds_list, date):
	list_funds_info = []
	fundcodes_failed = []
	for fcode in sub_funds_list:
		e = get_fund_price(fcode, date)
		if e == '-1':
			logger.warn("fetch fund code: %s failed", fcode)
			fundcodes_failed.append(fcode)
			continue

		t = (fcode, date, convert_str(e[1]), e[3], e[4], e[5], int(0))
		list_funds_info.append(t)
		time.sleep(SLEEP_TIME)

	# try again for fundcode that are fetched failed
	while len(fundcodes_failed) != 0:
		logger.info("try to fetch again, list of failed length: %s", len(fundcodes_failed))
		for ffailed in fundcodes_failed:
			e = get_fund_price(ffailed, date)
			if e == '-1':
				logger.error("fetch fund code: %s failed again", ffailed)
				continue
			logger.info("fetch again fund code: %s successfully", ffailed)

			t = (ffailed, date, convert_str(e[1]), e[3], e[4], e[5], int(0))
			list_funds_info.append(t)
			fundcodes_failed.remove(ffailed)
			time.sleep(SLEEP_TIME)


	return list_funds_info

# fund.eastmoney的ip地址
def get_domain_ip():
	ip_list = []
	A = dns.resolver.query(DOMAIN, 'A')
	for i in A.response.answer[2:]:
		for j in i.items:
			ip_list.append(j.to_text())

	return ip_list

def main(date):
	start_time = time.time()

	#yesterday = getYesterday()
	yesterday = date

	# get all fund code from db
	all_fundcodes = db.get_funds_list()

	'''
	# get al fund price informations
	# 计算需要多少线程
	funds_conut = len(all_fundcodes)
	m1 = funds_conut / NUMBER_PER_THREADING
	m2 = funds_conut % NUMBER_PER_THREADING
	if m2:
		threading_count = m1 + 1
	else:
		threading_count = m1
	'''
	threading_count = 1

	# TODO:  http://www.laitech.cn/2018/08/08/393/ python写一个多线程下载程序
	# 多线程获取基金情况
	list_result = []
	threads = []
	for i in range(threading_count):
		t = MyThread(fetch, args=(all_fundcodes, yesterday))
		threads.append(t)

	for t in threads:
		t.setDaemon(True)
		t.start()

	for t in threads:
		t.join()
		list_result.append(t.get_result())

	end_time = time.time()
	logger.info('spent time to get all funds: %s minites', (end_time - start_time) / 60 + 1)

	'''
	l = []
	for e in list_result:
		t = (fc, yesterday, convert_str(e[1]), e[3], e[4], e[5], int(0))
		l.append(t)
	'''
	# save into db
	db.batch_insert(db.TABLE_FUNDSTODAY, list_result[0])

	db.batch_insert_by_type(date)

	# to send message
	message = "fetch funds at %s successfully! 总共：%s 个基金" % (yesterday, len(list_result[0]))
	return message


# 此脚本为了获取单日基金情况，执行的时间为第二天的凌晨3：00，所以使用昨天的时间
if __name__ == "__main__":	
	reload(sys)
	sys.setdefaultencoding('utf-8')
	'''
	start_time = time.time()
	main('2020-02-24')
	end_time = time.time()
	print end_time - start_time
	'''







