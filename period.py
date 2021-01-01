# !/usr/bin/python
# -*- coding:utf-8 -*-

import db
import holiday
import datetime
import toml

config = toml.load('config.toml')

def period_range(from_date, today):
    email_datas = []
    for t in [db.TABLE_STOCK, db.TABLES_INDEX, db.TABLE_HYDIRD]:
        datas = []
        funds = db.get_funds_today(today, t)
        for f in funds:
            today_price = f[3] # 当日的累计净值
            code = f[1]
            fund_name = db.get_fundname_by_code(code)[0]

            # 查表获取一段时间内的最大值
            max_price_record = db.get_max_price(code, from_date, today)
            max_price = max_price_record[3]
            max_price_date = max_price_record[1]

            # 计算涨幅
            if max_price == float(0) or today_price == float(0):
                continue # 忽略价格为0的情况
            else:
                r = (float(today_price) - float(max_price)) / float(max_price) * 100
            row = (fund_name, code, max_price, max_price_date, r, 0)
            datas.append(row)
        # 批量更新funds_range_period表数据
        db.batch_insert_period(db.TABLE_RANGE_PERIOD, datas)

    limits = db.get_limit(db.TABLE_RANGE_PERIOD, "RangePeriod", config['value']['max'])
    for l in limits:
        # 最高点距离当天的天数
        days = (datetime.datetime.today() - datetime.datetime.strptime(l[3], "%Y-%m-%d")).days
        email_datas.append((l[1], l[0], l[3], l[2], l[4], days))
    return email_datas


def period_range_by_managers(from_date, today):
    email_datas = []
    funds = db.get_managers_funds()
    for f in funds:
        for ff in f:
            fff = ff.split(',')
            for code in fff:
                fundinfo = db.get_period_for_managers(code)
                days = (datetime.datetime.today() - datetime.datetime.strptime(fundinfo[3], "%Y-%m-%d")).days
                email_datas.append((fundinfo[1], fundinfo[0], fundinfo[3], fundinfo[2], fundinfo[4], days))

    return email_datas

if __name__ == "__main__":
    '''
    today = '2020-04-16'
    from_date = holiday.get_before_month_date(2)
    from_date = '2020-03-11'
    period_range(from_date, today)
    '''
    period_range_by_managers('2020-11-30', '2020-12-30')
