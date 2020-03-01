# !/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import sys
import datetime
import time



class MyThread(threading.Thread):
	def __init__(self, func, args = ()):
		super(MyThread, self).__init__()
		self.func = func
		self.args = args

	def run(self):
		self.result = self.func(*self.args)

	def get_result(self):
		try:
			return self.result
		except Exception:
			return None


n = 5

def thread_func(sub_list_my, i): # 线程函数
	#print( i, sub_list_my)
	return sub_list_my

def many_thread():
	threads = []
	list_result = []
	list_my = []
	# init list_my
	for i in range(22):
		list_my.append(i)

	#print list_my

	total = len(list_my)
	m1 = total / n
	m2 = total % n
	if m2:
		m1 = m1 + 1
	print m1

	#sys.exit()


	for i in range(m1): # 
		'''
		t = threading.Thread(target=thread_func(list_my[i*n:(i+1)*n]))
		threads.append(t)
		'''
		t = MyThread(thread_func, args=(list_my[i*n:(i+1)*n], i))
		threads.append(t)
		t.start()

	for t in threads: # 
		t.join()
		list_result.append(t.get_result())
	print list_result

if __name__ == '__main__':
	#many_thread()
	s = datetime.datetime.now()
	time.sleep(61.3)
	e = datetime.datetime.now()
	print (e - s).seconds / 60













