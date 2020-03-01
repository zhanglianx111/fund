# !/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import time

def run():

    time.sleep(2)
    print('main thread name:', threading.current_thread().name)
    time.sleep(2)


if __name__ == '__main__':

    start_time = time.time()

    print('this is mainthread:', threading.current_thread().name)
    thread_list = []
    for i in range(5):
        t = threading.Thread(target=run)
        thread_list.append(t)

    for t in thread_list:
        t.setDaemon(True)
        t.start()

    for t in thread_list:
        t.join()

    print('mainthread over:' , threading.current_thread().name)
    print('time:', time.time()-start_time)