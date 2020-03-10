# !/usr/bin/python
# -*- coding:utf-8 -*-


import rank_avg
import get_all_funds_today
import get_all_funds
import topN
import mail

import toml
import logging
import argparse
import datetime
import sys
import time

from logging.handlers import RotatingFileHandler
from db import TABLES_LIST

config = toml.load('config.toml')


logger = logging.getLogger("main")
logger.setLevel(level = config['log']['level'])

'''
handler = logging.FileHandler("funds.log")
handler.setLevel(config['log']['level'])
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s:%(lineno)d - %(message)s')
handler.setFormatter(formatter)
'''

# 日志回滚handler
rHandler = RotatingFileHandler("funds.log",maxBytes = 1*1024*1024,backupCount = 3)
rHandler.setLevel(config['log']['level'])
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s:%(lineno)d - %(message)s')
rHandler.setFormatter(formatter)


console = logging.StreamHandler()
console.setLevel(config['log']['level'])
console.setFormatter(formatter)

logger.addHandler(rHandler)
logger.addHandler(console)

# 给某一天的基金类型排名
def topn(date):
	logger.debug("sort at: %s", date)
	result = topN.main(date)

# 获取当天的基金情况
def fetchall(date):
	logger.info('fetch the fund net value of the date: %s', date)
	ret = get_all_funds_today.main(date)
	return ret

# 计算最近n天的排名平均值
def average():
	logger.info()

# 更新基金列表
def update_list():
	logger.info('start to update all funds list at %s', datetime.datetime.now())
	get_all_funds.main()
	logger.info('upate funds list finish.')

# print version information
def version():
	logger.info('version')
	print 'version: v1.0.1'

def range_for_date(flag, date):
	count = topN.range_greater_zero(flag, date)
	print count

# 获取某日某类型前count个基金
def get(fund_type, date, count):
	if int(fund_type) < 1 or int(fund_type) > 6:
		print "fund type error. 1 <= type <=6"
		sys.exit(1)
	ret = topN.get(fund_type, date, count)

	print(ret)
	return ret

# 获取一只基金在一段时间内的涨跌情况
def rise(fundcode, from_date, to_date):
	topN.get_rise_by_code(fundcode, from_date, to_date)

def routine(date):
	day = time.strftime("%w",time.localtime())
	if day == '0' or day == '1':
		logger.info('today is %s, have a rest!', time.strftime("%A",time.localtime()))
		sys.exit(1)

	message = ""

	# 获取当日的基金情况
	fetchall_ret = fetchall(date)
	message = message + fetchall_ret + "\n"

	# 单日涨跌基金个数
	# 上涨个数
	count = range_for_date(1, date)
	message = message + "上涨个数: " + str(count) + '\n'
	# 下跌个数
	count = range_for_date(-1, date)
	message = message + "下跌个数: " + str(count) + '\n'

	# 排名
	topn(date)

	# 获取排名
	count = 50
	for i in range(6):
		ret = get(i + 1, date, count)
		message =  message + TABLES_LIST[i+1] + '\n'
		message = message + str(ret) + '\n'


	# send email
	mail.send_email(message, date)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	subparsers = parser.add_subparsers()
	# sort all funds on someday
	parser_topn = subparsers.add_parser('topn', help='get top N of all funds nearly some days')
	parser_topn.set_defaults(action=('topn', topn))
	parser_topn.add_argument('--date', '-d', action="store", help="date for sorting", required=True)

	# get all funds info 
	parser_fetchall = subparsers.add_parser('fetchall', help='get all funds one day from fund.easymoney.com')
	parser_fetchall.set_defaults(action=('fetchall', fetchall))
	parser_fetchall.add_argument('--date', '-d', action='store', help="date to be fetch", required=True)

	# update funds list
	parser_update_funds_list = subparsers.add_parser('update_list', help='update funds list')
	parser_update_funds_list.set_defaults(action=('update_list', update_list))

	# 
	parser_range = subparsers.add_parser("range", help='range > 0 for range < 0')
	parser_range.set_defaults(action=('range', range_for_date))
	parser_range.add_argument('--date', '-d', action='store', help="date to get range", required=True)
	parser_range.add_argument('--flag', '-f', action='store', help="greater than zero or lesser than zero for range", required=True)

	#获取某日某类型前count个基金
	parser_get = subparsers.add_parser("get", help="获取某日或一段时间的某类型前count个基金")
	parser_get.set_defaults(action=('get', get))
	parser_get.add_argument('--type', '-t', action='store', help="type of the fund. \
		TABLES_LIST = [TALBE_FUNDSLIST, TABLE_FUNDSTODAY, TABLE_STOCK, TABLE_HYDIRD, TABLE_BOND, TABLE_FEEDER, TABLE_TIERED_LEVERAGED] \
		1: fundstoday 2: stock; 3:hybird; 4: bond; 5: feeder; 6: tieread_leveraaged", required=True)
	parser_get.add_argument('--date', '-d', action='store', help="date to get", required=True)
	parser_get.add_argument('--count', '-cnt', action='store', help="count of the fund for type", required=True)

	# 获取一只基金在一段时间内的涨跌情况
	parser_rise = subparsers.add_parser("rise", help="获取一只基金在一段时间内的涨跌情况")
	parser_rise.set_defaults(action=('rise', rise))
	parser_rise.add_argument('--from_date', '-fd', action='store', help="开始日期", required=True)
	parser_rise.add_argument('--to_date', '-td', action='store', help="结束日期", required=True)
	parser_rise.add_argument('--fundcode', '-fc', action='store', help="fund code to search", required=True)
	
	# 每天执行一次
	parser_routine = subparsers.add_parser('routine', help="每天例行执行")
	parser_routine.set_defaults(action=('routine', routine))
	parser_routine.add_argument('--date', '-d', action='store', help="routine every day", required=True)

	# version
	parser_version = subparsers.add_parser('version', help='print version information')
	parser_version.set_defaults(action=('version', version))


	args = parser.parse_args()
	logger.debug(args)
	(name, functor) = args.action

	if name in ['topn']:
		functor(args.date)

	if name in ['fetchall']:
		functor(args.date)
	
	if name in ['update_list']:
		functor()

	if name in ['version']:
		functor()

	if name in ['range']:
		functor(args.flag, args.date)

	if name in ['get']:
		functor(args.type, args.date, args.count)

	if name in ['routine']:
		functor(args.date)

	if name in ['rise']:
		functor(args.fundcode, args.from_date, args.to_date)

	'''
	parser = argparse.ArgumentParser(description="used for test")

	parser.add_argument('--version', '-v', action='version',
						version='%(prog)s version : v0.01', help='show the version')

	parser.add_argument('--debug', '-d', action='store_true',
						help='show the version',
						default=False)

	parser.add_argument('topn', type=int)

	args = parser.parse_args()
	print(args.topn)
	'''


