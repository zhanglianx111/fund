# !/usr/bin/python
# -*- coding:utf-8 -*-
import pymysql
import sys
import datetime
import string
import logging
import toml


config = toml.load('config.toml')

HOST = config['database']['host']
PORT = config['database']['port']
USER = config['database']['user']
PASSWD = config['database']['password']
DB = config['database']['db']
CHARSET = config['database']['charset']

TALBE_FUNDSLIST = 'funds_list' # 基金总列表
TABLE_FUNDSTODAY = 'funds_today' # 每日基金总表
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

TABLES_LIST = [TALBE_FUNDSLIST, TABLE_FUNDSTODAY, TABLE_STOCK, TABLE_HYDIRD, TABLE_BOND, TABLE_FEEDER, TABLE_TIERED_LEVERAGED]

logger = logging.getLogger('main.db')


def create_database():
	print HOST, PORT
	conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWD)
	with conn:
		sql = "create database %s" % DB
		cur = conn.cursor()
		cur.execute(sql)


def create_tables():
	conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWD, database=DB)

	sql_show_table = "show tables like %s"

	sql_create_table_fundslist = "create table if not exists %s( \
			FundCode VARCHAR(30) PRIMARY KEY, \
			ShortName VARCHAR(30), \
			FullName VARCHAR(100), \
			Type VARCHAR(30), \
			FullPinYin VARCHAR(100))ENGINE=InnoDB DEFAULT CHARSET=gbk"

	sql_create_table = "create table if not exists %s( \
							FundCode VARCHAR(30), \
							Date VARCHAR(30), \
							PriceToday FLOAT, \
							RangeToday VARCHAR(30), \
							BuyStatus VARCHAR(30), \
							SellStatus VARCHAR(30), \
							RankToday INT, \
							PRIMARY KEY(FundCode, Date))ENGINE=InnoDB DEFAULT CHARSET=gbk"

	#sql_two_key = "alter table %s add primary key(FundCode, Date)"

	with conn:
		cur = conn.cursor()
		try:
			for t in TABLES_LIST:
				if t == TALBE_FUNDSLIST:
					sql = sql_create_table_fundslist % t
				else:
					sql = sql_create_table % t

				if cur.execute(sql_show_table, t) == 0:
					cur.execute(sql)

		except Exception as err:
			print err


def batch_insert(table_name, datas):
	logger.debug(datas)
	conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWD, database=DB)

	if table_name == TALBE_FUNDSLIST:
		sql = "insert into %s( \
		FUNDCODE, \
		SHORTNAME, \
		FULLNAME, \
		TYPE, \
		FULLPINYIN) value('%s', '%s', '%s', '%s', '%s') on duplicate key update FUNDCODE=values(FUNDCODE)"
	else:	
		sql = "insert into %s( \
			FUNDCODE, \
			DATE, \
			PRICETODAY, \
			RANGETODAY, \
			BUYSTATUS, \
			SELLSTATUS, \
			RANKTODAY) value('%s', '%s', '%s', '%s', '%s', '%s', '%s') on duplicate key update FUNDCODE=values(FUNDCODE), DATE=values(DATE)"

	with conn:
		cur = conn.cursor()
		try:
			if len(datas[0]) == 5:		
				for d in datas:
					sql_insert = sql % (table_name, d[0], d[1], d[2], d[3], d[4])
					cur.execute(sql_insert)
			else:
				for d in datas:
					sql_insert = sql % (table_name, d[0], d[1], d[2], d[3], d[4], d[5], d[6])
					cur.execute(sql_insert)				

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
			sql = "select funds_today.* from funds_today left join `funds_list` on `funds_today`.FundCode = `funds_list`.FundCode \
					where `funds_list`.Type = %s and `funds_today`.Date = %s"
			try:
				cur.execute(sql, (t[0], date))
				rows = cur.fetchall()
				batch_insert(t[1], rows)
			
			except Exception as err:
				print err


def get_funds_list():
	conn = pymysql.connect(HOST, USER, PASSWD, DB)
	sql = "select * from funds_list"
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
				str(allrows[i][3]) == 'ETF-场内' or \
				str(allrows[i][3]) == '其他创新':
					continue
				fcode_list.append(allrows[i][0])

		except Exception as err:
			logger.error(err)

	return fcode_list


def get_funds_today(date_today, table_name):
	conn = pymysql.connect(HOST, USER, PASSWD, DB)
	sql = "select * from %s where Date = '%s'" % (table_name, date_today)

	with conn:
		cur = conn.cursor()
		try:
			count = cur.execute(sql)
			allrows = cur.fetchall()
			logger.info('get records count: %s on date: %s from table: %s', count, date_today, table_name)
			today = []
			for r in allrows:
				rise = r[3]
				rise = rise[:rise.index('%')]
				t = (string.atof(rise), r[0])
				today.append(t)

		except Exception as err:
			logger.error(err)	

	return today

def update_rank(ranklist, date, table_name):
	conn = pymysql.connect(HOST, USER, PASSWD, DB)
	sql = "update %s set RankToday = %s where FundCode = %s and Date = '%s'" 
	with conn:
		cur = conn.cursor()
		try:
			for r in ranklist:
				cur.execute(sql % (table_name, r[0], r[1], date))

			conn.commit()

		except Exception as err:
			logger.error(err)
			conn.rollback()

# 获取某天前n个涨幅最大的基金
def get_topn(n, date):
	conn = pymysql.connect(HOST, USER, PASSWD, DB)
	#sql = "select * from funds_today where Date = %s order by RankToday limit 0,%s"
	sql = "select funds_list.FullName, funds_today.* from funds_today left join `funds_list` on `funds_today`.FundCode = `funds_list`.FundCode where Date = %s order by RankToday limit 0,%s"
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
		sql = "select * from funds_today where Date = %s and RangeToday > %s"
	else:
		sql = "select * from funds_today where Date = %s and RangeToday < %s"

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
	#datas = [('000001', '2020-02-26', 1.197, '-3.78%', '开放申购', '开放赎回', 0), ('000002', '2020-02-26', -1.197, '-1.72%', '开放申购', '开放赎回', 0)]
	#batch_insert(TABLE_FUNDSTODAY, datas)
	#flist = get_funds_list()
	#get_funds_today()

	#######################
	#batch_insert(t, datas)

	#batch_insert_by_type('2020-03-05')








