# !/usr/bin/python
# -*- coding:utf-8 -*-
import pymysql
import sys
import datetime
import string
import logging

HOST = '127.0.0.1'
PORT = 3306
USER = 'root'
PASSWD = 'pw'
DB = 'funds'
CHARSET = 'utf8'

TALBE_FUNDSLIST = 'fundslist' # 基金总列表
TABLE_FUNDSTODAY = 'fundstoday' # 每日基金总表
TABLE_HYDIRD = 'funds_hybird' # 混合型每日总表
TABLE_STOCK = 'funds_stock' # 股票型每日总表
TABLE_BOND = 'funds_bond' # 债券型每日总表
TABLE_FEEDER = 'funds_feeder' # 联接基金
TABLE_TIERED_LEVERAGED = 'funds_tiered_leveraged'  # 分级杠杆基金

FUNDCODE = 'FundCode' # 基金代码
SHORTNAME = 'ShortName' # 基金名简拼
FULLNAME = 'FullName' # 基金全名 中文
TYPE = 'Type' # 基金类型
FULLPINYIN = 'FullPinYin' # 基金名全拼
DATE = 'Date' # 日期
PRICETODAY = 'PriceToday' # 当日净值
RANGETODAY  = 'RangeToday' # 当日涨幅
BUYSTATUS = 'BuyStatus' # 申购状态
SELLSTATUS = 'SellStatus' # 赎回状态
RANKTODAY = 'RankToday' # 今日排名

logger = logging.getLogger('main.db')

def batch_insert(table_name, datas):
	logger.debug(datas)
	conn = pymysql.connect(HOST, USER, PASSWD, DB)

	if table_name == TALBE_FUNDSLIST:
		sql = "insert into fundslist( \
		FUNDCODE, \
		SHORTNAME, \
		FULLNAME, \
		TYPE, \
		FULLPINYIN) value(%s, %s, %s, %s, %s) on duplicate key update FUNDCODE=values(FUNDCODE)"
		
	'''
	if table_name == TABLE_FUNDSTODAY:
		sql = "insert into fundstoday( \
		FUNDCODE, \
		DATE, \
		PRICETODAY, \
		RANGETODAY, \
		BUYSTATUS, \
		SELLSTATUS, \
		RANKTODAY) value(%s, %s, %s, %s, %s, %s, %s) on duplicate key update FUNDCODE=values(FUNDCODE) && DATE=values(DATE)"
	'''

	if table_name == TABLE_FUNDSTODAY:
		sql = "insert into fundstoday( \
		FUNDCODE, \
		DATE, \
		PRICETODAY, \
		RANGETODAY, \
		BUYSTATUS, \
		SELLSTATUS, \
		RANKTODAY) value(%s, %s, %s, %s, %s, %s, %s)"

	if table_name == TABLE_HYDIRD:
		sql = "insert into funds_hybird( \
		FUNDCODE, \
		DATE, \
		PRICETODAY, \
		RANGETODAY, \
		BUYSTATUS, \
		SELLSTATUS, \
		RANKTODAY) value(%s, %s, %s, %s, %s, %s, %s)"

	if table_name == TABLE_STOCK:
		sql = "insert into funds_stock( \
		FUNDCODE, \
		DATE, \
		PRICETODAY, \
		RANGETODAY, \
		BUYSTATUS, \
		SELLSTATUS, \
		RANKTODAY) value(%s, %s, %s, %s, %s, %s, %s)"

	if table_name == TABLE_BOND:
		sql = "insert into funds_bond( \
		FUNDCODE, \
		DATE, \
		PRICETODAY, \
		RANGETODAY, \
		BUYSTATUS, \
		SELLSTATUS, \
		RANKTODAY) value(%s, %s, %s, %s, %s, %s, %s)"
	
	if table_name == TABLE_FEEDER:
		sql = "insert into funds_feeder( \
		FUNDCODE, \
		DATE, \
		PRICETODAY, \
		RANGETODAY, \
		BUYSTATUS, \
		SELLSTATUS, \
		RANKTODAY) value(%s, %s, %s, %s, %s, %s, %s)"
	
	if table_name == TABLE_TIERED_LEVERAGED:
		sql = "insert into funds_tiered_leveraged( \
		FUNDCODE, \
		DATE, \
		PRICETODAY, \
		RANGETODAY, \
		BUYSTATUS, \
		SELLSTATUS, \
		RANKTODAY) value(%s, %s, %s, %s, %s, %s, %s)"
	
		

	with conn:
		cur = conn.cursor()

		# 创建表
		# table fundslist
		sql_table_fundslist = "show tables like 'fundslist'"
		if cur.execute(sql_table_fundslist) == 0:
			print 'table: fundslist is not exist, create it'
			cur.execute("create table if not exists fundslist( \
				FundCode VARCHAR(30) PRIMARY KEY, \
				ShortName VARCHAR(30), \
				FullName VARCHAR(100), \
				Type VARCHAR(30), \
				FullPinYin VARCHAR(100))ENGINE=InnoDB DEFAULT CHARSET=gbk")
		
		# table fundstoday
		sql_table_fundstoday = "show tables like 'fundstoday'"
		if cur.execute(sql_table_fundstoday) == 0:
			print 'table: fundstoday is not exist, create it'
			cur.execute("create table if not exists fundstoday( \
				FundCode VARCHAR(30), \
				Date VARCHAR(30), \
				PriceToday FLOAT, \
				RangeToday VARCHAR(30), \
				BuyStatus VARCHAR(30), \
				SellStatus VARCHAR(30), \
				RankToday INT)")
				#PRIMARY KEY(FundCode, Date)")
		
		sql_table_funds_hybird = "show tables like 'funds_hybird'"
		if cur.execute(sql_table_funds_hybird) == 0:
			print 'table: funds_hybird is not exist, create it'
			cur.execute("create table if not exists funds_hybird( \
				FundCode VARCHAR(30), \
				Date VARCHAR(30), \
				PriceToday FLOAT, \
				RangeToday VARCHAR(30), \
				BuyStatus VARCHAR(30), \
				SellStatus VARCHAR(30), \
				RankToday INT)")

		sql_table_funds_stock = "show tables like 'funds_stock'"
		if cur.execute(sql_table_funds_stock) == 0:
			print 'table: funds_stock is not exist, create it'
			cur.execute("create table if not exists funds_stock( \
				FundCode VARCHAR(30), \
				Date VARCHAR(30), \
				PriceToday FLOAT, \
				RangeToday VARCHAR(30), \
				BuyStatus VARCHAR(30), \
				SellStatus VARCHAR(30), \
				RankToday INT)")

		sql_table_funds_bond = "show tables like 'funds_bond'"
		if cur.execute(sql_table_funds_bond) == 0:
			print 'table: funds_bond is not exist, create it'
			cur.execute("create table if not exists funds_bond( \
				FundCode VARCHAR(30), \
				Date VARCHAR(30), \
				PriceToday FLOAT, \
				RangeToday VARCHAR(30), \
				BuyStatus VARCHAR(30), \
				SellStatus VARCHAR(30), \
				RankToday INT)")

		sql_table_funds_feeder = "show tables like 'funds_feeder'"
		if cur.execute(sql_table_funds_feeder) == 0:
			print 'table: funds_feeder is not exist, create it'
			cur.execute("create table if not exists funds_feeder( \
				FundCode VARCHAR(30), \
				Date VARCHAR(30), \
				PriceToday FLOAT, \
				RangeToday VARCHAR(30), \
				BuyStatus VARCHAR(30), \
				SellStatus VARCHAR(30), \
				RankToday INT)")

		sql_table_funds_tiered_leveraged = "show tables like 'funds_tiered_leveraged'"
		if cur.execute(sql_table_funds_tiered_leveraged) == 0:
			print 'table: funds_tiered_leveraged is not exist, create it'
			cur.execute("create table if not exists funds_tiered_leveraged( \
				FundCode VARCHAR(30), \
				Date VARCHAR(30), \
				PriceToday FLOAT, \
				RangeToday VARCHAR(30), \
				BuyStatus VARCHAR(30), \
				SellStatus VARCHAR(30), \
				RankToday INT)")

		try:
			#for d in datas:
			cur.executemany(sql, datas)
			conn.commit()
			logger.info('insert date into table[%s] count: %d successfully!', \
						table_name, len(datas))

		except Exception as err:
			logger.error(err)
			conn.rollback()

# 按基金类型存入不同的表
def batch_insert_by_type(date):
	conn = pymysql.connect(HOST, USER, PASSWD, DB)

	type_list = [('股票型', TABLE_STOCK), \
				 ('混合型', TABLE_HYDIRD), \
				 ('债券型', TABLE_BOND), \
				 ('联接基金', TABLE_FEEDER), \
				 ('分级杠杆', TABLE_TIERED_LEVERAGED)]
	with conn:
		cur = conn.cursor()

		for t in type_list:
			sql = "select fundstoday.* from fundstoday left join `fundslist` on `fundstoday`.FundCode = `fundslist`.FundCode \
					where `fundslist`.Type = %s and `fundstoday`.Date = %s"
			try:
				cur.execute(sql, (t[0], date))
				rows = cur.fetchall()
				batch_insert(t[1], rows)
			
			except Exception as err:
				print err


def get_funds_list():
	conn = pymysql.connect(HOST, USER, PASSWD, DB)
	sql = "select * from fundslist"
	with conn:
		cur = conn.cursor()
		try:
			count = cur.execute(sql)
			allrows = cur.fetchall()

			fcode_list = []
			for i in range(count):
				if str(allrows[i][3]) == '货币型' or \
				str(allrows[i][3]) == '理财型' or \
				str(allrows[i][3]) == '定开债券' or \
				str(allrows[i][3]) == '保本型' or \
				str(allrows[i][3]) == '固定收益' or \
				str(allrows[i][3]) == '分级杠杆' or \
				str(allrows[i][3]) == 'ETF-场内' or \
				str(allrows[i][3]) == '货币型' or \
				str(allrows[i][3]) == '其他创新':
					continue
				fcode_list.append(allrows[i][0])

		except Exception as err:
			logger.error(err)

	return fcode_list


def get_funds_today(date_today):
	conn = pymysql.connect(HOST, USER, PASSWD, DB)
	sql = "select * from fundstoday where Date = %s"
	with conn:
		cur = conn.cursor()
		try:
			count = cur.execute(sql, date_today)
			allrows = cur.fetchall()
			logger.info('get records count: %s on date: %s from table: %s', count, date_today, TABLE_FUNDSTODAY)
			today = []
			for r in allrows:
				rise = r[3]
				rise = rise[:rise.index('%')]
				t = (string.atof(rise), r[0])
				today.append(t)

		except Exception as err:
			logger.error(err)	

	return today

def update_fundstoday_rank(ranklist, date):
	conn = pymysql.connect(HOST, USER, PASSWD, DB)
	sql = "update fundstoday set RankToday = %s where FundCode = %s and Date = %s"
	with conn:
		cur = conn.cursor()
		try:
			for r in ranklist:
				cur.execute(sql,(r[0], r[1], date))

			conn.commit()

		except Exception as err:
			logger.error(err)
			conn.rollback()

# 获取某天前n个涨幅最大的基金
def get_topn(n, date):
	conn = pymysql.connect(HOST, USER, PASSWD, DB)
	#sql = "select * from fundstoday where Date = %s order by RankToday limit 0,%s"
	sql = "select fundslist.FullName, fundstoday.* from fundstoday left join `fundslist` on `fundstoday`.FundCode = `fundslist`.FundCode where Date = %s order by RankToday limit 0,%s"
	with conn:
		cur = conn.cursor()
		try:
			cur.execute(sql, (date, int(n)))
			records = cur.fetchall()



		except Exception as err:
			logger.error(err)

	return records

# 获取date日涨幅>0或<0的基金数
def get_greater_zero(flag, date):
	conn = pymysql.connect(HOST, USER, PASSWD, DB)

	if flag == '1':
		sql = "select * from fundstoday where Date = %s and RangeToday > %s"
	else:
		sql = "select * from fundstoday where Date = %s and RangeToday < %s"

	with conn:
		cur = conn.cursor()
		try:
			count = cur.execute(sql, (date,'0.00%'))

		except Exception as err:
			logger.error(err)
			return -1

		return count


def get_topn_by_type(fund_type, date, count):
	conn = pymysql.connect(HOST, USER, PASSWD, DB)

	print fund_type, date, count

	sql = "select fundslist.FullName, `%s`.* from `%s` left join `fundslist` on `%s`.FundCode = `fundslist`.FundCode where Date = %s order by RankToday limit 0, %s"

	with conn:
		cur = conn.cursor()
		sql_table = "show tables like '%s'" % TABLE_STOCK
		print cur.execute(sql_table)
		cur.execute(sql, (TABLE_BOND, TABLE_BOND, TABLE_BOND, date, int(count)))
		result = cur.fetchall()
		print result


if __name__ ==  "__main__":
	print __name__
	#t = TALBE_FUNDSLIST

	# for test
	#datas = [('q1', 'w1', 's1', 'r1', 't1'), ('q2', 'w2', 's2', 'r2', 't2')]
	#datas = [('000001', '2020-02-26', 1.197, '-3.78%', '代理费', '是否', 0)]
	#batch_insert(TABLE_FUNDSTODAY, datas)
	#flist = get_funds_list()
	#get_funds_today()

	#######################
	#batch_insert(t, datas)

	batch_insert_by_type('2020-03-03')








