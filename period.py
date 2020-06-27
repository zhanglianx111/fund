# !/usr/bin/python
# -*- coding:utf-8 -*-

import db
import holiday

def period_range(from_date, today):
    for t in [db.TABLE_STOCK, db.TABLES_INDEX, db.TABLE_HYDIRD]:
        datas = []
        funds = db.get_funds_today(today, t)
        for f in funds:
            today_price = f[2]
            code = f[1]

            # 查表获取一段时间内的最大值
            max_price_record = db.get_max_price(code, from_date, today)
            max_price = max_price_record[2]
            max_price_date = max_price_record[1]

            # 计算涨幅
            if max_price == float(0) or today_price == float(0):
                continue # 忽略价格为0的情况
            else:
                r = (float(today_price) - float(max_price)) / float(max_price) * 100

            datas.append((code, max_price, max_price_date, r, 0))

        # 批量更新funds_range_period表数据
        db.batch_insert_period(db.TABLE_RANGE_PERIOD, datas)

if __name__ == "__main__":
    today = '2020-04-16'
    from_date = holiday.get_before_month_date(2)
    from_date = '2020-03-11'
    period_range(from_date, today)