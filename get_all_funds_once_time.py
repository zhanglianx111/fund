#!/usr/bin/env python
# -*- coding:utf-8 -*-


import requests
import json
import re
import logging
import db
import toml
from bs4 import BeautifulSoup
from logging.handlers import RotatingFileHandler
from datetime import timedelta, datetime

config = toml.load('config.toml')


logger = logging.getLogger("main.get_all_funds_once_time")
logger.setLevel(level = config['log']['level'])

# 日志回滚handler
rHandler = RotatingFileHandler("funds.log",maxBytes = 1*1024*1024,backupCount = 3)
rHandler.setLevel(config['log']['level'])
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s:%(lineno)d - %(message)s')
rHandler.setFormatter(formatter)


console = logging.StreamHandler()
console.setLevel(config['log']['level'])
console.setFormatter(formatter)

logger.addHandler(rHandler)
logger.addHandler(console)

def get_all_funds_datas(date):
    yesterday = date
    all_funds = []  
    # 原始url: 
    url_page = 'http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx?t=1&lx=1&letter=&gsid=&text=&sort=zdf,desc&page=1,&atfc=&onlySale=0'
    rawhtml = requests.get(url_page)

    postion_conut = rawhtml.text.find('count')
    a = rawhtml.text[:postion_conut]
    b = a[::-1].replace(",", "}", 1)[::-1]
   
    c = b.split('=')[1]
    datas_map = json.loads(c.replace('chars', '"chars"').replace('datas', '"datas"').replace('count', '"count"'))
    '''
    for i in range(len(datas_map['datas'])):	
        fund = (datas_map['datas'][i][0], \
            datas_map['datas'][i][1], \
            datas_map['datas'][i][3], \
            datas_map['datas'][i][4], \
            datas_map['datas'][i][8])

        all_funds.append(fund)
    '''
    for data in datas_map['datas']:
        if len(data[4]) != 0 and data[8] != "":
            fund = (data[0], yesterday, data[3], data[4], data[8]+"%", data[9], data[10], 0)
            all_funds.append(fund)

    #print all_funds
    db.batch_insert(db.TABLE_FUNDSTODAY, all_funds)
    db.batch_insert_by_type(yesterday)

    # to send message
    message = "fetch funds at %s successfully! 总共：%s 个基金" % (yesterday, len(all_funds))
    return message


if __name__ == '__main__':
    yesterday = datetime.today() + timedelta(-1)
    
    yesterday_format = yesterday.strftime('%Y-%m-%d')
    get_all_funds_datas(yesterday_format)
