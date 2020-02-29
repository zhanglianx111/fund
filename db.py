# !/usr/bin/python
# -*- coding:utf-8 -*-
import pymysql
import sys
import datetime
import string

HOST = '127.0.0.1'
PORT = 3306
USER = 'root'
PASSWD = 'pw'
DB = 'funds'
CHARSET = 'utf8'
TALBE_FUNDSLIST = 'fundslist' # 基金列表
TABLE_FUNDSTODAY = 'fundstoday' # 每日基金情况

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


def batch_insert(table_name, datas):
	print datas
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
		
		try:
			cur.executemany(sql, datas)
			conn.commit()
			print '%s: insert date into table[%s] count: %d successfully for %s!' % ( \
				datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'), table_name, len(datas))

		except Exception as err:
			print(err)
			conn.rollback()


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
				str(allrows[i][3]) == '固定收益':
					continue
				fcode_list.append(allrows[i][0])

				'''
				# for test
				if i == 50:
					break
				'''
		except Exception as err:
			print '111'
			print __name__, err	

	return fcode_list


def get_funds_today(date_today):
	conn = pymysql.connect(HOST, USER, PASSWD, DB)
	sql = "select * from fundstoday where Date = %s"
	with conn:
		cur = conn.cursor()
		try:
			count = cur.execute(sql, date_today)
			allrows = cur.fetchall()
			print len(allrows)
			print count
			today = []
			for r in allrows:
				rise = r[3]
				rise = rise[:rise.index('%')]
				t = (string.atof(rise), r[0])
				today.append(t)

		except Exception as err:
			print '1111'
			print(err)	


	return today

def update_fundstoday_rank(ranklist):
	conn = pymysql.connect(HOST, USER, PASSWD, DB)
	sql = "update fundstoday set RankToday = %s where FundCode = %s"
	with conn:
		cur = conn.cursor()
		try:
			for r in ranklist:
				cur.execute(sql,(r[0], r[1]))

			conn.commit()

		except Exception as err:
			print(err)
			conn.rollback()

if __name__ ==  "__main__":
	t = TALBE_FUNDSLIST

	# for test
	#datas = [('q1', 'w1', 's1', 'r1', 't1'), ('q2', 'w2', 's2', 'r2', 't2')]
	#datas = [('000001', '2020-02-26', 1.197, '-3.78%', '代理费', '是否', 0)]
	#batch_insert(TABLE_FUNDSTODAY, datas)
	#flist = get_funds_list()
	#get_funds_today()

	#######################
	batch_insert(t, datas)










