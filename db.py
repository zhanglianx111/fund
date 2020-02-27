# !/usr/bin/python
# -*- coding:utf-8 -*-
import pymysql
import sys

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
	conn = pymysql.connect(HOST, USER, PASSWD, DB)

	if table_name == TALBE_FUNDSLIST:
		sql = "insert into fundslist( \
		FUNDCODE, \
		SHORTNAME, \
		FULLNAME, \
		TYPE, \
		FULLPINYIN) value(%s, %s, %s, %s, %s) on duplicate key update FUNDCODE=values(FUNDCODE)"
		
		#sql = "update fundslist set "

		#insert into test_tbl (id,dr) values (1,'2'),(2,'3'),...(x,'y') on duplicate key update dr=values(dr);

	if table_name == TABLE_FUNDSTODAY:
		sql = "insert into fundstoday(FUNDCODE, \
		DATE, \
		PRICETODAY, \
		RANGETODAY, \
		BUYSTATUS, \
		SELLSTATUS, \
		RANKTODAY) value(%s, %s, %s, %s, %s, %s, %s)"

	#cursor = conn1.cursor()
	# 创建表
	#cursor.execute("CREATE TABLE IF NOT EXISTS Writers(Id INT PRIMARY KEY AUTO_INCREMENT,Name VARCHAR(25))")
	conn.cursor().execute("create table if not exists fundslist( \
		FundCode VARCHAR(30) PRIMARY KEY, \
		ShortName VARCHAR(30), \
		FullName VARCHAR(100), \
		Type VARCHAR(30), \
		FullPinYin VARCHAR(255))ENGINE=InnoDB DEFAULT CHARSET=gbk")



	conn.cursor().execute("create table if not exists fundstoday( \
		FundCode VARCHAR(30) PRIMARY KEY, \
		Date DATE, \
		PriceToday FLOAT, \
		RangeToday FLOAT, \
		BuyStatus VARCHAR(30), \
		SellStatus VARCHAR(30), \
		RankToday INT)")

	with conn:
		cur = conn.cursor()
		#sql = "insert into %s(Name) value(%s)"
		try:
			cur.executemany(sql, datas)
			conn.commit()

		except Exception as err:
			print(err)


if __name__ ==  "__main__":
	t = TALBE_FUNDSLIST
	# for test
	datas = [('q1', 'w1', 's1', 'r1', 't1'), ('q2', 'w2', 's2', 'r2', 't2')]
	batch_insert(t, datas)











