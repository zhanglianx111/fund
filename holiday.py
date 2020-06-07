# -*- coding:utf-8 -*-
import datetime
import sys
import logging

logger = logging.getLogger('main.db')


'''以下是统计2019年and2020年节假日'''
'''节假日和周六、日不开市'''

'''判断当天日期是否为节假日'''

#把调休的休息日加到这里面
rest_holiday=[
    '2020-01-01','2020-01-24','2020-01-27','2020-01-28','2020-01-29','2020-01-30',
    '2020-04-06','2020-05-01','2020-05-04','2020-05-05','2020-06-25','2020-06-26',
    '2020-10-01','2020-10-02','2020-10-05','2020-10-06','2020-10-07','2020-10-08',
    '2021-01-01',
]
#把调休的工作日加到这里面
rest_workday=[
    '2019-02-02','2019-02-03','2019-04-27','2019-02-28','2019-09-29','2019-10-12',
    '2019-12-28','2019-12-29',
    '2020-01-19','2020-02-01','2020-06-28','2020-09-27','2020-10-10',
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



if __name__=='__main__':
    print sys.argv[1]
    is_holiday_or_weedday(sys.argv[1])