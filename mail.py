# !/usr/bin/python
# -*- coding:utf-8-*-

# 配置： config.toml
#		包括：邮箱地址
#			 收件人
# 接口： 给谁发送什么内容

import get_all_funds_today

import smtplib
import logging
import toml
from db import TABLES_LIST
from prettytable import PrettyTable


from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger('main.mail')

def send_email(funds_totol, datas, date):
    config = toml.load('config.toml')

    sender = config['mail']['sender'] # 发送者邮箱地址
    sender_pass = config['mail']['sender_password'] #

    # 自己发给自己
    receiver = sender

    # 设置总的邮件体对象，对象类型为mixed
    msg_root = MIMEMultipart('mixed')

    # 邮件添加的头尾信息等
    msg_root['From'] = config['mail']['sender']
    msg_root['To'] = receiver

    # 邮件的主题，显示在接收邮件的预览页面，以日期为邮件主题
    #subject = get_all_funds_today.getYesterday()
    subject = "基金daily " + date
    msg_root['subject'] = Header(subject, 'utf-8')

    '''
    # 构造文本内容
    text_info = message
    text_sub = MIMEText(text_info, 'plain', 'utf-8')
    msg_root.attach(text_sub)
    '''

    html_data = format_datas(funds_totol, datas)
    msg_root.attach(html_data)
    #message = format_datas(datas)
    # 把构造的内容写到邮件体中
    #msg_root.attach(message)

    try:
        s = smtplib.SMTP()
        s.connect(config['mail']['server'])
        s.login(sender, sender_pass)
        s.sendmail(sender, receiver, msg_root.as_string())
        s.quit()

    except Exception as e:
        logger.error('sendemail failed, the reason: %s', e)
        return

    logger.info("mail sended ok at %s" % date)

def format_datas(counts, fund_datas):
    msg = '<span>上涨基金数: %s</span>' % counts[0] + '\n'
    msg += '<span>下跌基金数: %s</span>' % counts[1]
    html_tables = msg

    for i in range(7):
        jjmc = []
        jjdm = []
        rq = []
        jz = []
        zf = []
        pm = []
        datas = {'基金名称': [], '基金代码': [], '日期': [], '净值': [], '涨幅': [], '排名': []}

        for f in fund_datas[str(i+1)]:
            jjmc.append(f[0])
            jjdm.append(f[1])
            rq.append(f[2])
            jz.append(f[3])
            zf.append(f[4])
            pm.append(f[7])

        datas['基金名称'] = jjmc
        datas['基金代码'] = jjdm
        datas['日期'] = rq
        datas['净值'] = jz
        datas['涨幅'] = zf
        datas['排名'] = pm


        #keys = datas.keys()
        keys = ['基金名称', '基金代码', '日期', '净值', '涨幅', '排名']
        length = len(datas[keys[0]])

        items = ['<span style="font-size:16px;"><td><strong>表名: %s</strong></td></span>' % TABLES_LIST[i+1]]
        items += ['<table style="width:700px">', '<tr>']
        for k in keys:
            items.append('<td>%s</td>' % k)
        items.append('</tr>')

        for j in range(length):
            items.append('<tr>')
            for k in keys:
                items.append('<td>%s</td>' % datas[k][j])
            items.append('</tr>')

        items.append('</table>')

        html_tables += '\n'.join(items)

    html_sub = MIMEText(html_tables, 'html', 'utf-8')
    return html_sub


if __name__ == '__main__':
    # 可以是一个列表，支持多个邮件地址同时发送，测试改成自己的邮箱地址
    #content = '你好' + '\t' + 'age' + '\t' + 'male' + '\n' + '张三' + '\t' + '18' + '\t' + '男'
    #content = "hello \n funds: %s count: %s at: %s" % ('stock', 233, '2020-01-01')
    #send_email(content, '2020-01-01')

    x= PrettyTable(["姓名", "年龄", "籍贯"])
    x.add_row(["张三",32,"北京"])
    x.add_row(["李四",45,"天津"])
    x.add_row(["王五",28,"河北"])
    m = str(x)
    print m
    send_email(m, '表格')






