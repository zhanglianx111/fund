# !/usr/bin/python
# -*- coding:utf-8 -*-


import rank_avg
import get_all_funds_today
import get_all_funds
import topN
#import version

import toml
import logging
import argparse
import datetime
import sys
from logging.handlers import RotatingFileHandler

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

# 给某一天的所有基金排名
def topn(number, days):
	logger.debug("topN n: %s, days: %s", number, days)
	if number == None:
		logger.info('sort all funds at date: %s', days)
	else:
		logger.info("start to sort the first %s funds at date: %s.", number, days)
		need_print = True

	result = topN.main(number, days)

	if need_print:
		print '基金代码' + '\t' + '日期' + '\t\t' + '净值' + '\t\t' + '涨幅' + '\t\t' + '排名' 

		for r in result:
			print r[0] + '\t\t' + r[1] + '\t' + str(r[2]) + '\t\t' + r[3] + '\t\t' + str(r[6])


# 获取当天的基金情况
def fetchall(date):
	logger.info('fetch the fund net value of the date: %s', date)
	get_all_funds_today.main(date)

# 计算最近n天的排名平均值
def average():
	logger.info()

# 更新基金列表
def update_list():
	logger.info('start to update all funds list at %s', datetime.datetime.now())
	#get_all_funds.main()
	logger.info('upate funds list finish.')

# print version information
def version():
	logger.info('ccca')
	print 'version: v1.0.1'

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers()

	# sort all funds on someday
	parser_topn = subparsers.add_parser('topn', help='get top N of all funds nearly some days')
	parser_topn.set_defaults(action=('topn', topn))
	parser_topn.add_argument('--number', '-n', action="store", help="get the first n record, if number is empty, sort all. \
		n >= 1", required=False)
	parser_topn.add_argument('--days', '-d', action="store", help="days to top", required=True)

	# get all funds info 
	parser_fetchall = subparsers.add_parser('fetchall', help='get all funds one day from fund.easymoney.com')
	parser_fetchall.set_defaults(action=('fetchall', fetchall))
	parser_fetchall.add_argument('--date', '-d', action='store', help="date to be fetch", required=True)

	# update funds list
	parser_update_funds_list = subparsers.add_parser('update_list', help='update funds list')
	parser_update_funds_list.set_defaults(action=('update_list', update_list))

	# version
	parser_version = subparsers.add_parser('version', help='print version information')
	parser_version.set_defaults(action=('version', version))


	args = parser.parse_args()
	logger.debug(args)
	(name, functor) = args.action
	
	if name in ['topn']:
		functor(args.number, args.days)

	if name in ['fetchall']:
		functor(args.date)
	
	if name in ['update_list']:
		functor()

	if name in ['version']:
		functor()

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


