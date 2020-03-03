# !/usr/bin/python 
# -*- coding: utf-8 -*-

import db

import datetime
import logging
import sys
import time

logger = logging.getLogger("main.topN")


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


def main(number, date_today):
	'''
	t = datetime.date.today()  
	date_today = datetime.datetime.strftime(t, '%Y-%m-%d')	
	logger.info("today: %s", date_today)
	sys.exit()
	'''
	topn_records = []
	start_time = time.time()
	if number == None:  # 所有基金排名
		today = db.get_funds_today(date_today)
		sort_today = QuickSort(today, 0, len(today) -1)
		ranklist = ranking(sort_today)
		db.update_fundstoday_rank(ranklist, date_today)
		logger.info('rank all funds complitly.')
	else: # 查找涨幅前n个基金
		logger.info('get the first %s record', number)
		need_return = True
		topn_records = get_first_n(number, date_today)

	end_time = time.time()
	logger.info('spent time to sort funds: %s minites', (end_time - start_time) / 60 + 1)

	return topn_records

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

