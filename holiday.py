# -*- coding:utf-8 -*-
import datetime
import sys

'''以下是统计2019年and2020年节假日'''
'''节假日和周六、日不开市'''

'''判断当天日期是否为节假日'''

#把调休的休息日加到这里面
rest_holiday=[
    '2020-01-01','2020-01-24','2020-01-27','2020-01-28','2020-01-29','2020-01-30',
    '2020-04-06','2020-05-01','2020-05-04','2020-05-05''2020-06-25','2020-06-26',
    '2020-10-01','2020-10-02','2020-10-05','2020-10-06','2020-10-07','2020-10-08',
    '2021-01-01',
]
#把调休的工作日加到这里面
rest_workday=[
    '2019-02-02','2019-02-03','2019-04-27','2019-02-28','2019-09-29','2019-10-12',
    '2019-12-28','2019-12-29',
    '2020-01-19','2020-02-01','2020-06-28','2020-09-27','2020-10-10',
]

def is_holiday_or_weedday(current_date):
    set_date = datetime.datetime.strptime(current_date,"%Y-%m-%d")

    #0~6代表周一~周日
    weekday=set_date.weekday()
    print weekday
    if weekday in [5, 6]:
        print current_date, 'is weedend'
        return True


    if current_date in rest_holiday:
        print current_date, 'is holiday'
        return True

    return False


if __name__=='__main__':
    print sys.argv[1]
    is_holiday_or_weedday(sys.argv[1])
    '''
    try:
        start_date='2019-01-01'
        end_date='2021-01-01'
        is_holiday(start_date,end_date)
    except Exception as e:
        import traceback
        ex_msg = '{exception}'.format(exception=traceback.format_exc())
        print(ex_msg,e)
    '''