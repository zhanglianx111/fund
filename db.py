# !/usr/bin/python
# -*- coding:utf-8 -*-

import sys
sys.path.insert(0,"/usr/local/lib/python2.7/site-packages")
import pymysql
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

# 表名
TALBE_FUNDSLIST = 'funds_list' 		# 基金总列表
TABLE_FUNDSTODAY = 'funds_today' 	# 每日基金总表
TABLE_HYDIRD = 'funds_hybird' 		# 混合型每日总表
TABLE_STOCK = 'funds_stock' 		# 股票型每日总表
TABLE_BOND = 'funds_bond' 			# 债券型每日总表
TABLE_BOND_DINGKAI = 'funds_bond_dingkai' #定开债券
TABLE_FEEDER = 'funds_feeder' 		# 联接基金
TABLES_INDEX = 'funds_index'		# 股票指数基金
TABLE_TIERED_LEVERAGED = 'funds_tiered_leveraged' 	# 分级杠杆基金
TABLE_QDII = 'funds_qdii'           # QDII基金
TABLE_RANGE_PERIOD = 'funds_range_period' # 记录一段时间内的最大净值，和当前时间的净值做比较，计算涨跌幅

SUFFIX = 'percentage'
TABLE_STOCK_PERCENTAGE = TABLE_STOCK + "_" + SUFFIX
TABLES_INDEX_PERCENTAGE = TABLES_INDEX + "_" + SUFFIX
TABLE_HYDIRD_PERCENTAGE = TABLE_HYDIRD + "_" + SUFFIX
TABLE_BOND_PERCENTAGE = TABLE_BOND + "_" + SUFFIX
TABLE_BOND_DINGKAI_PERCENTAGE = TABLE_BOND_DINGKAI + "_" + SUFFIX
TABLE_FEEDER_PERCENTAGE = TABLE_FEEDER + "_" + SUFFIX
TABLE_TIERED_LEVERAGED_PERCENTAGE = TABLE_TIERED_LEVERAGED + "_" + SUFFIX
TABLE_QDII_PERCENTAGE = TABLE_QDII + "_" + SUFFIX

# 基金类型-表名 对应列表
TYPE_LIST = [('股票型', TABLE_STOCK), \
				 ('股票指数', TABLES_INDEX), \
				 ('混合型', TABLE_HYDIRD), \
				 ('债券型', TABLE_BOND), \
			 	 ('定开债券', TABLE_BOND_DINGKAI), \
				 ('联接基金', TABLE_FEEDER), \
				 ('分级杠杆', TABLE_TIERED_LEVERAGED), \
				 ('QDII', TABLE_QDII) \
			]

# 表字段名
FUNDCODE = 'FundCode' 		# 基金代码
SHORTNAME = 'ShortName' 	# 基金名简拼
FULLNAME = 'FullName' 		# 基金全名 中文
TYPE = 'Type' 				# 基金类型
FULLPINYIN = 'FullPinYin' 	# 基金名全拼
DATE = 'Date' 				# 日期
FROMDATE = 'FromDate' 		# 开始日期
TODATE = 'ToDate'			# 结束日期
PRICETODAY = 'PriceToday' 	# 当日净值
PRICEALLDAY = 'PriceAllDay'	# 累计净值
RANGETODAY  = 'RangeToday' 	# 当日涨幅
RANGEWEEK = 'RangeWeek'		# 每周涨幅
BUYSTATUS = 'BuyStatus' 	# 申购状态
SELLSTATUS = 'SellStatus' 	# 赎回状态
RANKTODAY = 'RankToday' 	# 今日排名
RANKWEEK = 'RankWeek'		# 本周排名
MAXPRICE = 'MaxPrice'		# 最大净值
RANGEPERIOD = 'RangePeriod' # 周期涨跌幅
BUYRANGE = 'BuyRange'		# 买入到跌幅值

TABLES_LIST = [TALBE_FUNDSLIST, TABLE_STOCK, TABLES_INDEX, TABLE_HYDIRD, TABLE_BOND, TABLE_BOND_DINGKAI, TABLE_FEEDER, \
			   TABLE_TIERED_LEVERAGED, TABLE_QDII, TABLE_FUNDSTODAY]
TABLES_LIST_PERCENTAGE = [TABLE_STOCK_PERCENTAGE, TABLES_INDEX_PERCENTAGE, TABLE_HYDIRD_PERCENTAGE, TABLE_BOND_PERCENTAGE,
						  TABLE_BOND_DINGKAI_PERCENTAGE, TABLE_FEEDER_PERCENTAGE, TABLE_TIERED_LEVERAGED_PERCENTAGE, TABLE_QDII_PERCENTAGE]

logger = logging.getLogger('main.db')

conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWD, db=DB)


def create_database():
	print HOST, PORT
	#conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWD)
	with conn:
		sql = "create database %s" % DB
		cur = conn.cursor()
		cur.execute(sql)


def create_tables_percentage():
	sql_show_table = "show tables like %s"
	sql_create_table = "create table if not exists %s( \
							FullName VARCHAR(100), \
							FundCode VARCHAR(30), \
							FromDate VARCHAR(30), \
							ToDate VARCHAR(30), \
							RangeWeek VARCHAR(30), \
							RandWeek INT, \
							PRIMARY KEY(FundCode, FromDate))ENGINE=InnoDB DEFAULT CHARSET=gbk"
	with conn:
		cur = conn.cursor()
	try:
		for t in TABLES_LIST_PERCENTAGE:
			sql = sql_create_table % t
			if cur.execute(sql_show_table, t) == 0:
				cur.execute(sql)

	except Exception as err:
		logger.error(err)

def create_tables():
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
							PriceAllDay FLOAT, \
							RangeToday VARCHAR(30), \
							BuyStatus VARCHAR(30), \
							SellStatus VARCHAR(30), \
							RankToday INT, \
							PRIMARY KEY(FundCode, Date))ENGINE=InnoDB DEFAULT CHARSET=gbk"

	sql_create_table_funds_range_period = "create table if not exists %s( \
										  FundCode VARCHAR(30) PRIMARY KEY, \
										  MaxPrice FLOAT, \
										  Date VARCHAR(30), \
										  RangePeriod FLOAT , \
										  BuyRange FLOAT)ENGINE=InnoDB DEFAULT CHARSET=gbk"
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
			# 创建周期涨跌幅表
			if cur.execute(sql_show_table, TABLE_RANGE_PERIOD) == 0:
				sql = sql_create_table_funds_range_period % TABLE_RANGE_PERIOD
				cur.execute(sql)

		except Exception as err:
			logger.error(err)


def batch_insert_percentage(table_name, datas):
	logger.debug(datas)

	sql = "insert into %s( \
		FULLNAME, \
		FUNDCODE, \
		FROMDATE, \
		TODATE, \
		RANGEWEEK, \
		RANKWEEK) value('%s', '%s', '%s', '%s', '%s', '%s') on duplicate key update FUNDCODE=values(FUNDCODE), FROMDATE=values(FROMDATE)"

	with conn:
		cur = conn.cursor()
		try:
			for d in datas:
				sql_insert = sql % (table_name, d[0], d[1], d[2], d[3], d[4], d[5])
				cur.execute(sql_insert)

			conn.commit()
			logger.info('insert date into table[%s] count: %d successfully!', \
						table_name, len(datas))

		except Exception as err:
			logger.error(err)
			conn.rollback()

def batch_insert(table_name, datas):
#	logger.debug(datas)

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
			PRICEALLDAY, \
			RANGETODAY, \
			BUYSTATUS, \
			SELLSTATUS, \
			RANKTODAY) value('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s') on duplicate key update FUNDCODE=values(FUNDCODE), DATE=values(DATE)"

	with conn:
		cur = conn.cursor()
		try:
			if len(datas[0]) == 5:
				# clean funds_list table
				cur.execute("delete from %s" % TALBE_FUNDSLIST)
				for d in datas:
					sql_insert = sql % (table_name, d[0], d[1], d[2], d[3], d[4])
					cur.execute(sql_insert)
			else:
				for d in datas:
					sql_insert = sql % (table_name, d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7])
					cur.execute(sql_insert)				

			conn.commit()
			logger.info('insert date into table[%s] count: %d successfully!', \
						table_name, len(datas))

		except Exception as err:
			logger.error(err)
			conn.rollback()

def batch_insert_period(table_name, datas):
	sql = "replace into %s( \
		FULLNAME, \
		FUNDCODE, \
		MAXPRICE, \
		DATE, \
		RANGEPERIOD, \
		BUYRANGE) value('%s', '%s', '%f', '%s', '%.3f', '%.2g')"

	with conn:
		cur = conn.cursor()
		try:
			for d in datas:
				sql_insert = sql % (table_name, d[0], d[1], d[2], d[3], d[4], d[5])
				cur.execute(sql_insert)

			conn.commit()
			logger.info('insert date into table[%s] count: %d successfully!', \
						table_name, len(datas))

		except Exception as err:
			logger.error(err)
			conn.rollback()

# 表内基金的个数
def get_list_count(table_name, date):
	if table_name == TALBE_FUNDSLIST:
		sql = "select * from funds_list"
	elif table_name == TABLE_FUNDSTODAY:
		#yestoday = datetime.datetime.strftime(datetime.date.today() + datetime.timedelta(-1), '%Y-%m-%d')
		sql = "select * from %s where Date = '%s'" %(TABLE_FUNDSTODAY, date)
	else:
		if table_name == TABLE_STOCK:
			type1 = '股票型'
		elif table_name == TABLES_INDEX:
			type1 = '股票指数'
		elif table_name == TABLE_HYDIRD:
			type1 = '混合型'
		elif table_name == TABLE_BOND:
			type1 = '债券型'
		elif table_name == TABLE_FEEDER:
			type1 = '联接基金'
		elif table_name == TABLE_TIERED_LEVERAGED:
			type1 = '分级杠杆'
		elif table_name == TABLE_QDII:
			type1 = 'QDII'
		elif table_name == TABLE_BOND_DINGKAI:
			type1 = '定开债券'
		else:
			logger.warning("not supported table name")
			return 0

		sql = "select * from funds_list where Type = '%s'" % type1

	with conn:
		try:
			cur = conn.cursor()
			count = cur.execute(sql)
			return count
		except Exception as err:
			logger.error(err)



# 按基金类型存入不同的表
def batch_insert_by_type(date):
	with conn:
		cur = conn.cursor()

		for t in TYPE_LIST:
			sql = "select funds_today.* from funds_today left join `funds_list` on `funds_today`.FundCode = `funds_list`.FundCode \
					where `funds_list`.Type = %s and `funds_today`.Date = %s"
			try:
				cur.execute(sql, (t[0], date))
				rows = cur.fetchall()
				batch_insert(t[1], rows)
			
			except Exception as err:
				logger.error(err)


def get_funds_list():
	sql = "select * from funds_list"
	fcode_list = []
	with conn:
		cur = conn.cursor()
		try:
			count = cur.execute(sql)
			allrows = cur.fetchall()

			for i in range(count):
				if str(allrows[i][3]) == '货币型' or \
				str(allrows[i][3]) == '理财型' or \
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
	#conn = pymysql.connect(HOST, USER, PASSWD, DB)
	sql = "select * from %s where Date = '%s'" % (table_name, date_today)
	today = []

	with conn:
		cur = conn.cursor()
		try:
			count = cur.execute(sql)
			allrows = cur.fetchall()
			logger.info('get records count: %s on date: %s from table: %s', count, date_today, table_name)
			for r in allrows:
				rise = r[4]
				rise = rise[:rise.index('%')]
				t = (string.atof(rise), r[0], r[2], r[3])
				today.append(t)

		except Exception as err:
			logger.error(err)

	return today

def update_rank(ranklist, date, table_name):
	#conn = pymysql.connect(HOST, USER, PASSWD, DB)
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
	#conn = pymysql.connect(HOST, USER, PASSWD, DB)
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
	#conn = pymysql.connect(HOST, USER, PASSWD, DB)
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
	#conn = pymysql.connect(HOST, USER, PASSWD, DB)
	table = TABLES_LIST[int(fund_type)]

	sql = "select funds_list.FullName, %s.* from %s left join funds_list on %s.FundCode = funds_list.FundCode where Date = '%s' order by RankToday limit 0, %s" % \
			(table, table, table, date, int(count))

	with conn:
		cur = conn.cursor()
		#sql_table = "show tables like '%s'" % TABLE_STOCK
		#print cur.execute(sql_table)
		cur.execute(sql)
		result = cur.fetchall()

	return result

# 由基金代码找到对应存储的表名
def get_table_by_fundcode(fundcode):
	#conn = pymysql.connect(HOST, USER, PASSWD, DB)
	sql = "select Type from funds_list where FundCode = '%s'" % fundcode

	with conn:
		cur = conn.cursor()
		cur.execute(sql)
		atype = cur.fetchone()
		if atype is None:
			return None

		ftable = atype[0]
		if ftable == '股票型':
			return TABLE_STOCK
		if ftable == '股票指数':
			return  TABLES_INDEX
		if ftable == '混合型':
			return TABLE_HYDIRD
		if ftable == '联接基金':
			return TABLE_FEEDER
		if ftable == '债券型':
			return TABLE_BOND
		if ftable == '分级杠杆':
			return TABLE_TIERED_LEVERAGED
		if ftable == '定开债券':
			return TABLE_BOND_DINGKAI
		if ftable == 'QDII':
			return TABLE_QDII
		else:
			return None

def get_fundcode_by_table(table_name):
	#conn = pymysql.connect(HOST, USER, PASSWD, DB)
	sql = "select distinct %s from %s" % (FUNDCODE, table_name)
	with conn:
		cur = conn.cursor()
		cur.execute(sql)
		fcs = cur.fetchall()

	return fcs

# 一只基金在一段时间内的数据。
# 数据包括：日期、涨幅、排名
# return: ('累计涨跌幅度', '涨次数', '跌次数', '最大涨幅', '最大跌幅', '平均排名')
def get_rise_by_code(fundcode, table_name, start_date, end_date):
	sql = "select %s, %s, %s from %s where FundCode = '%s' and Date >= '%s' and Date <= '%s'" % (DATE, RANGETODAY, RANKTODAY, table_name, fundcode, start_date, end_date)
	with conn:
		try:
			cur = conn.cursor()
			cur.execute(sql)
			rows = cur.fetchall()

			range_totol = float(0)	# 累计涨幅
			riseCount = 0		# 上涨次数
			downCount = 0		# 下跌次数
			range_max = ()		# 上涨最大信息
			range_min = ()		# 下跌最大信息
			rank_avg  = 0		# 平均排名
			max_range = 0		# 涨幅最大
			min_range = 0		# 跌幅最大
			rank_totol = 0		# rank总和

			length = len(rows)
			if length == 0:
				return None
			for i in range(length):
				rng = float(str(rows[i][1]).split('%')[0])
				if rng > 0:
					riseCount+=1
					if rng > max_range:
						max_range = rng
						range_max = rows[i]
				if rng < 0:
					downCount+=1
					if rng < min_range:
						min_range = rng
						range_min = rows[i]

				rank_totol+=rows[i][2]
				# TODO 修改涨幅的计算方法： (price_enddate - price_startdate) / priice_startdate
				'''
				range_totol += rng
				if abs(range_totol - 0.00001) <= 0.0001:
					range_totol = float(0.0)
				'''
			# price_enddate
			sql = "select PriceToday from %s where FundCode = '%s' and Date = '%s'" % (table_name, fundcode, end_date)
			cur.execute(sql)
			price_enddate = cur.fetchone()
			if price_enddate is None:
				return None
			else:
				price_e = price_enddate[0]

			# price_startdate
			sql = "select PriceToday from %s where FundCode = '%s' and Date = '%s'" % (table_name, fundcode, start_date)
			cur.execute(sql)
			price_startdate = cur.fetchone()
			if price_startdate is None:
				return None
			else:
				price_s = price_startdate[0]

			if price_s == 0 or price_e == 0:
				return None

			range_totol = (float(price_e) - float(price_s)) / float(price_s)

		except Exception as err:
			logger.error(err)

		return (fundcode, float(format(range_totol, '.4f'))*100, riseCount, downCount, range_max, range_min, rank_totol/length)

def get_fundname_by_code(fundcode):
	#conn = pymysql.connect(HOST, USER, PASSWD, DB)
	sql = "select FullName from funds_list where FundCode = %s" % fundcode	
	with conn:
		cur = conn.cursor()
		cur.execute(sql)
		name = cur.fetchone()
		return name

# 复制所有表的src_date记录到dest_date中
def copy(src_date, dest_date):
	logger.info("start to copy from %s to %s", src_date, dest_date)
	with conn:
		cur = conn.cursor()
		for t in TABLES_LIST[1:]:
			sql_get = "select * from %s where Date = '%s'" % (t, src_date)
			cur.execute(sql_get)
			src_rows = cur.fetchall()
			if len(src_rows) == 0:
				return
			list_rows = list(src_rows)
			list_tmp = []
			for r in list_rows:
				r = r[:1] + (dest_date,) + r[2:]
				list_tmp.append(r)
			dest_rows = tuple(list_tmp)
			batch_insert(t, dest_rows)

# 一段时间内的最大净值
def get_max_price(fund_code, from_date, to_date):
	with conn:
		cur = conn.cursor()
		# 获取从from_date到to_date期间到最大值
		sql = "select * from funds_today where FundCode = %s and \
			Date between '%s' and '%s' \
			order by PriceAllDay desc limit 1" % (fund_code, from_date, to_date)

		cur.execute(sql)
		arecord = cur.fetchone()
		return arecord

# 按字段排序
def get_limit(table_name, field, limit):
	with conn:
		cur = conn.cursor()
		sql = "select * from %s  where `%s` < %s order by %s" % (table_name, field, limit, field)
		cur.execute(sql)
		rst = cur.fetchall()
		return rst

# 统计一段时间内处于前n%基金的出现的次数
'''select count(*) as count, `FULLNAME` from funds_index_percentage group by FULLNAME order by count'''


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

	#batch_insert_by_type('2020-02-26')
	#get_rise_by_code('000082', TABLE_STOCK, '2020-03-09', '2020-03-09')
	create_database()
	create_tables_percentage()
	create_tables()







