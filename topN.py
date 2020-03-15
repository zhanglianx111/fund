# !/usr/bin/python 
# -*- coding: utf-8 -*-

import db

import datetime
import logging
import sys
import time
from prettytable import PrettyTable

logger = logging.getLogger("main.topN")

sys.setrecursionlimit(1000000) #递归深度设置为一百万  

# 从大到小排序
# input: [(rangetoday, 'fundcode')]
# output: 按rangetoday排好序的数组[(rangetoday, 'fundcode')]
def QuickSort(myList,start,end):
    #判断low是否小于high,如果为false,直接返回
    if start < end:
        i,j = start,end
        #设置基准数
        base = myList[i]

        while i < j:
            #如果列表后边的数,比基准数大或相等,则前移一位直到有比基准数小的数出现
            while (i < j) and (myList[j] <= base):
                j = j - 1

            #如找到,则把第j个元素赋值给第个元素i,此时表中i,j个元素相等
            myList[i] = myList[j]

            #同样的方式比较前半区
            while (i < j) and (myList[i] >= base):
                i = i + 1
            myList[j] = myList[i]
        #做完第一轮比较之后,列表被分成了两个半区,并且i=j,需要将这个数设置回base
        myList[i] = base

        #递归前后半区
        QuickSort(myList, start, i - 1)
        QuickSort(myList, j + 1, end)

    return myList

# 连续相等的长度
def eq(sub_sort_list):
	i = 0
	length = len(sub_sort_list)

	while i < length - 1:
		if  sub_sort_list[i][0] == sub_sort_list[i+1][0]:
			i = i + 1
		else:
			break

	return i + 1


# 给排序后的数组贴上rank标签
# input: 排行序的数组[(rangetoday, 'fundcode')]
# output: [(rank, 'fundcode', range)]
def ranking(sort_list):
	rank_list = []
	length = len(sort_list)
	
	i = 0 # i 记录sort_list中的位置
	j = 1 # j 记录rank位置
	try:
		while i < length - 1:
			if sort_list[i][0] == sort_list[i+1][0]:
				sub_length = eq(sort_list[i:])
				for sub_index in range(sub_length):
					t = (j, sort_list[i+sub_index][1], sort_list[i+sub_index][0])
					rank_list.append(t)

				i = i + sub_length

				if i == length - 1:
					break 
			else:
				t = (j, sort_list[i][1], sort_list[i][0])
				rank_list.append(t)
				i = i + 1

			j = j + 1

		# last one
		if i == length - 1:	
			t = (j+1, sort_list[i][1], sort_list[i][0])
			rank_list.append(t)

	except StandardError, e:
		logger.error("error: %s", e)

	return rank_list


def get_first_n(n, date):
	return db.get_topn(n, date)


def range_greater_zero(flag, date):
	return db.get_greater_zero(flag, date)


def main(date_today):
	'''
	t = datetime.date.today()  
	date_today = datetime.datetime.strftime(t, '%Y-%m-%d')	
	logger.info("today: %s", date_today)
	sys.exit()
	'''

	start_time = time.time()

	for t in db.TABLES_LIST[1:]:
		today = db.get_funds_today(date_today, t)
		sort_today = QuickSort(today, 0, len(today) -1)
		ranklist = ranking(sort_today)
		db.update_rank(ranklist, date_today, t)

		logger.info('rank funds of table[%s] complitly.', t)

	end_time = time.time()

	logger.info('spent time to sort funds: %s minites', (end_time - start_time) / 60 + 1)


def get(fund_type, date, count):
	ret = db.get_topn_by_type(fund_type, date, count)

	x = PrettyTable(["基金名称", "基金代码", "日期", "净值", "涨幅", "排名"])
	for f in ret:
		x.add_row([f[0], f[1], f[2], f[3], f[4], f[7]])
	return x

def get_rise_by_code(fundcode, start_date, end_date):
	table_name = db.get_table_by_fundcode(fundcode)
	if table_name == None:
		return None

	ret = db.get_rise_by_code(fundcode, table_name, start_date, end_date)
	if ret != None:
		return ret
	else:
		return None

def QuickSort_for_allcode(myList,start,end):
	#print myList
	#判断low是否小于high,如果为false,直接返回
	if start < end:
		i,j = start,end
		#设置基准数
		#print myList[i]
		base = myList[i]

		while i < j:
			#如果列表后边的数,比基准数大或相等,则前移一位直到有比基准数小的数出现
			while (i < j) and (myList[j][1] <= base[1]):
				j = j - 1

			#如找到,则把第j个元素赋值给第个元素i,此时表中i,j个元素相等
			myList[i] = myList[j]

			#同样的方式比较前半区
			while (i < j) and (myList[i][1] >= base[1]):
				i = i + 1
			myList[j] = myList[i]
		#做完第一轮比较之后,列表被分成了两个半区,并且i=j,需要将这个数设置回base
		myList[i] = base

		#递归前后半区
		QuickSort_for_allcode(myList, start, i - 1)
		QuickSort_for_allcode(myList, j + 1, end)

	return myList




def get_rise_by_allcode(table_name, from_date, to_date):
	rise_list = []
	# 根据表名获取表中基金代码
	codes = db.get_fundcode_by_table(table_name)
	for c in codes:
		r = get_rise_by_code(c[0], from_date, to_date)
		if r != None:
			rise_list.append(r)

	sort_result = QuickSort_for_allcode(rise_list, 0, len(rise_list) -1)

	t_header = PrettyTable(['序号','基金代码','累计涨跌幅度', '涨次数', '跌次数', '最大涨幅信息', '最大跌幅信息', '平均排名'])
	length = len(sort_result)
	for i in range(length):
		r = sort_result[i]
		if r != None:
			t_header.add_row([str(i+1), r[0], r[1], r[2], r[3], r[4], r[5], r[6]])

	return t_header



if __name__ == '__main__':

	#myList = [(0.0,'000001'),(-0.32,'000002'),(1.23,'000003'),(0.3,'000004'),(1.23,'000005'),(-2.3,'000006'),(0.72,'000007'), \
	#(-2.3,'000008'),(1.23,"000009"),(-2.3,'000010')]
	#print("Quick Sort: ")
	#sort_list = QuickSort(myList,0,len(myList)-1)
	#print sort_list
	#print ranking(sort_list)

	
	# ==============
	#main()
	print range_greater_zero(1, '2020-03-02')

