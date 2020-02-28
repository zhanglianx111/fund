# !/usr/bin/python 
# -*- coding: utf-8 -*-

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

# 给排序后的数组贴上rank标签
# input: 排行序的数组[(rangetoday, 'fundcode')]
# output: [('fundcode', rank)]
def get_rank(sort_list):
	rank_list = []
	length = len(sort_list)

	# i 记录sort_list中的位置
	# j 记录rank位置
	i = 0
	j = 1
	while i < length - 1:
		if sort_list[i][0] > sort_list[i+1][0]:
			t = (j, sort_list[i][1], sort_list[i][0])
			j = j + 1
			rank_list.append(t)
		else:
			t = (j, sort_list[i][1], sort_list[i][0])
			rank_list.append(t)
		i = i + 1

	return rank_list


if __name__ == '__main__':

	myList = [(0.0,'000001'),(-0.32,'000002'),(1.23,'000003'),(0.3,'000004'),(-1.4,'000005'),(0.3,'000006'),(0.72,'000007'),(-2.3,'000008')]
	print("Quick Sort: ")
	sort_list = QuickSort(myList,0,len(myList)-1)
	print get_rank(sort_list)

