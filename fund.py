# !/usr/bin/python
# -*- coding:utf-8 -*-


import get_all_funds_today
import get_all_funds
import topN
import mail
from db import TABLES_LIST
from db import TABLES_LIST_PERCENTAGE
import db
import holiday
import period

import toml
import logging
import argparse
import datetime
import sys
import time
from prettytable import PrettyTable
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

# 给某一天的基金类型排名
def topn(date):
    logger.debug("sort at: %s", date)
    result = topN.main(date)

# 获取当天的基金情况
def fetchall(date):
    logger.info('========================== %s ========================', date)
    logger.info('fetch the fund net value of the date: %s', date)
    ret = get_all_funds_today.main(date)
    print ret

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
    return count

# 获取某日某类型前count个基金
def get(fund_type, date, count):
    if int(fund_type) < 1 or int(fund_type) > len(TABLES_LIST):
        print "fund type index error."
        sys.exit(1)
    ret = topN.get(fund_type, date, count)
    '''
    # insert into table of db
    if int(fund_type) - 1 < len(TABLES_LIST_PERCENTAGE):
        db.batch_insert_percentage(db.TABLES_LIST_PERCENTAGE[int(fund_type) - 1], ret)
    '''
    return ret

# 获取一只基金在一段时间内的涨跌情况
def rise_by_one(fundcode, from_date, to_date):
    if to_date is None:
        # 使用当天的日期
        to_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')

    ret = topN.get_rise_by_code(fundcode, from_date, to_date)
    if ret is None:
        print "未找到基金"
        sys.exit(1)
    else:
        t = PrettyTable(['基金代码', '累计涨跌幅度', '涨次数', '跌次数', '最大涨幅信息', '最大跌幅信息', '平均排名'])
        t.add_row([ret[0], ret[1], ret[2], ret[3], ret[4], ret[5], ret[6]])
        print t


def rise_by_all(table, from_date, to_date, flag):
    if to_date is None:
        # 使用当天的日期
        to_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')

    if flag == 0:
        ret = topN.get_rise_by_allcode(table, from_date, to_date, flag)

        # 打印表数据
        print ret[0]
        print '基金总数: ', ret[1]
    else:
        topN.get_rise_by_allcode(table, from_date, to_date, flag)

def routine(date):
    # 如果是节假日或周末，复制前一天的数据
    if holiday.is_holiday_or_weekend(args.date):
        dest_date = datetime.date.today() - datetime.timedelta(days=1)
        src_date = dest_date - datetime.timedelta(days=1)
        db.copy(src_date, dest_date)


        sys.exit(0)

    # 获取当日的基金情况
    today = fetchall(date)

    # 单日涨跌基金个数
    # 上涨个数
    count1 = range_for_date('1', date)
    # 下跌个数
    count2 = range_for_date('-1', date)

    # 排名
    topn(date)

    # 获取排名
    mail_datas = {}
    period_datas = {}
    length = len(db.TABLES_LIST) - 1
    for i in range(len(TABLES_LIST[1:length-1])):
        tcount = db.get_list_count(TABLES_LIST[i+1], date)
        if tcount == 0:
            logger.warning(TABLES_LIST[i+1])
            continue
        percent = int(tcount * config['percent']['percent'])

        ret = get(i + 1, date, percent)
        mail_datas[str(i+1)] = ret

    # 周六计算本周各基金涨幅情况
    if datetime.date.today().weekday() == 5:
        pre_friday, friday = holiday.get_current_week()
        logger.info("pre friday = %s, friday = %s", pre_friday, friday)
        for t in db.TABLES_LIST[1:length]:
            rise_by_all(t, pre_friday, friday, True)

    # 计算一段时间内的涨跌幅
    from_date = holiday.get_before_month_date(config['period']['months'])
    period_datas[str(1)] = period.period_range(from_date, date)
    mail.send_email([0, len(period_datas[str(1)])], period_datas, date)

    # send email
    mail.send_email([count1, count2], mail_datas, date)

# origin_date: %m.%d
# format: %y-%m-%d
def format_date(origin_date):
    if origin_date is None:
        return None

    list_date = origin_date.split('.')
    m = int(list_date[0])
    d = int(list_date[1])
    if 0 < m < 10:
        month = '0' + str(m)
    else:
        month = str(m)

    if 0 < d < 10:
        day = '0' + str(d)
    else:
        day = str(d)

    return str(datetime.datetime.now().year) + '-' + month + '-' + day


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
        TABLES_LIST = [TALBE_FUNDSLIST, TABLE_STOCK, TABLES_INDEX, TABLE_HYDIRD, TABLE_BOND, TABLE_BOND_DINGKAI, TABLE_FEEDER, TABLE_TIERED_LEVERAGED, TABLE_QDII, TABLE_FUNDSTODAY] \
            1: stock; 2:stock_index; 3:hybird; 4: bond; 5: bond_dingkai; 6: feeder; 7: tieread_leveraaged; 8: qdii", required=True)
    parser_get.add_argument('--date', '-d', action='store', help="date to get", required=True)
    parser_get.add_argument('--count', '-cnt', action='store', help="count of the fund for type", required=True)

    # 获取一只基金在一段时间内的涨跌情况
    parser_rise = subparsers.add_parser("rise_by_one", help="获取一只基金在一段时间内的涨跌情况")
    parser_rise.set_defaults(action=('rise_by_one', rise_by_one))
    parser_rise.add_argument('--from_date', '-fd', action='store', help="开始日期", required=True)
    parser_rise.add_argument('--to_date', '-td', action='store', help="结束日期")
    parser_rise.add_argument('--fundcode', '-fc', action='store', help="fund code to search", required=True)
    

    # 获取某类型基金在一段时间内的涨跌情况
    parser_rise = subparsers.add_parser("rise_all_by_type", help="获取某类型基金在一段时间内的涨跌情况")
    parser_rise.set_defaults(action=('rise_all_by_type', rise_by_all))
    parser_rise.add_argument('--from_date', '-fd', action='store', help="开始日期", required=True)
    parser_rise.add_argument('--to_date', '-td', action='store', help="结束日期")
    parser_rise.add_argument('--table', '-t', action='store', help="table name. e.g. 1: funds_stock 2: funds_index; 3:funds_hybird; 4: funds_bond; 5: funds_bond_dingkai; \
    6: funds_feeder; 7: funds_tiered_leveraged; 8:funds_qdii", required=True)
    parser_rise.add_argument('--flag', '-f', action='store_true', help="flag=true 代表计算每周涨幅", required=False)

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

    if name != 'version' and name != 'update_list' and name != 'rise_by_one' and name != 'rise_all_by_type':
        args.date = format_date(args.date)

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

    if name in ['rise_by_one']:
        args.from_date = format_date(args.from_date)
        args.to_date = format_date(args.to_date)
        functor(args.fundcode, args.from_date, args.to_date)

    if name in ['rise_all_by_type']:
        args.from_date = format_date(args.from_date)
        args.to_date = format_date (args.to_date)
        functor(args.table, args.from_date, args.to_date, args.flag)

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


