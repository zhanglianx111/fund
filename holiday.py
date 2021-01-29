# -*- coding:utf-8 -*-
import datetime
import sys
import logging
from dateutil.relativedelta import relativedelta

logger = logging.getLogger('main.holiday')


'''以下是统计2019年and2020年节假日'''
'''节假日和周六、日不开市'''

'''判断当天日期是否为节假日'''

#把调休的休息日加到这里面
rest_holiday=[
    '2021-01-01','2021-02-12','2021-02-13','2021-02-14','2021-02-15','2021-02-16',
    '2021-02-17','2021-04-05','2021-04-06','2021-04-07','2021-05-01','2021-05-02',
    '2021-05-03','2021-05-04','2021-05-05','2021-06-14','2021-06-15','2021-06-16',
    '2021-09-21','2021-10-01','2021-10-02','2021-10-03','2021-10-04','2021-10-05'
    '2021-10-06','2021-10-07'
]

def is_holiday_or_weekend(current_date):
    set_date = datetime.datetime.strptime(current_date,"%Y-%m-%d")

    #0~6代表周一~周日
    weekday=set_date.weekday()

    if weekday in [5, 6]:
        logger.info("%s is weekend", current_date)
        return True


    if current_date in rest_holiday:
        logger.info("%s is holiday", current_date)
        return True

    return False


def get_current_week():
    today = datetime.date.today().weekday()
    monday, friday = datetime.date.today(), datetime.date.today()
    one_day = datetime.timedelta(days=1)

    while monday.weekday() != 0:
        monday -= one_day

    # 上周五的日期
    pre_friday = (monday - 3*one_day)
    # 本周五日期
    if today >= 5:
        while friday.weekday() != 4:
            friday -= one_day
    else:
        while friday.weekday() != 4:
            friday += one_day
    # 返回当前的上周五和本周五的日期
    return pre_friday, friday

# 计算今天之前n个月之前的日期
def get_before_month_date(mons):
    before_today = datetime.date.today() - relativedelta(months=mons)
    return before_today

if __name__=='__main__':
    print sys.argv[1]
    is_holiday_or_weedday(sys.argv[1])
