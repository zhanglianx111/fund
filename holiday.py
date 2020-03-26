# -*- coding:utf-8 -*-
import datetime

'''以下是统计2019年and2020年节假日'''
'''节假日和周六、日不开市'''

'''判断当天日期是否为节假日'''

#把调休的休息日加到这里面
rest_holiday=[
    '2018-12-31',
    '2019-01-01','2019-02-04','2019-02-05','2019-02-06','2019-02-07','2019-02-08',
    '2019-04-05','2019-04-29','2019-04-30','2019-05-01','2019-06-07','2019-09-13',
    '2019-10-01','2019-10-02','2019-10-03','2019-10-04','2019-10-07','2019-12-30',
    '2019-12-31',
    '2020-01-01','2020-01-24','2020-01-27','2020-01-28','2020-01-29','2020-01-30',
    '2020-04-06','2020-05-01','2020-06-25','2020-06-26','2020-10-01','2020-10-02',
    '2020-10-05','2020-10-06','2020-10-07','2020-10-08',
    '2021-01-01',
]
#把调休的工作日加到这里面
rest_workday=[
    '2019-02-02','2019-02-03','2019-04-27','2019-02-28','2019-09-29','2019-10-12',
    '2019-12-28','2019-12-29',
    '2020-01-19','2020-02-01','2020-06-28','2020-09-27','2020-10-10',
]

def is_holiday(start_date,end_date):
    set_date = datetime.datetime.strptime(start_date,"%Y-%m-%d")
    for i in range(10000):
        set_date_str=set_date.strftime('%Y-%m-%d')
        if set_date_str>=end_date:
            break
        #0~6代表周一~周日
        weekday=set_date.weekday()
        if set_date_str in rest_holiday or (weekday in [5,6] and set_date_str not in rest_workday):
            is_holiday=1
            is_monday=0
        else:
            is_holiday = 0
            is_monday = 1
        #这里的sql语句可根据自己的需要进行调整
        sql="INSERT INTO dmdc.t_is_holiday(`date`,is_holiday,is_monday) VALUES ('%s',%s,%s);"%(set_date_str,is_holiday,is_monday)
        #把sql语句写入sql文件
        with open('./date_is_holiday.sql','a+') as f:
            f.write(sql+'\n')
        #日期加1
        set_date = set_date + datetime.timedelta(days=1)


if __name__=='__main__':
    try:
        start_date='2019-01-01'
        end_date='2021-01-01'
        is_holiday(start_date,end_date)
    except Exception as e:
        import traceback
        ex_msg = '{exception}'.format(exception=traceback.format_exc())
        print(ex_msg,e)
