# !/usr/bin/python
# -*- coding:utf-8-*-

# 配置： config.toml
#		包括：邮箱地址
#			 收件人
# 接口： 给谁发送什么内容

import get_all_funds_today

import smtplib
import logging
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger('main.mail')

def to_send_message():
    return 'hello world'

def send_email():
    config = toml.load('config.toml')

    sender_mail = config['mail']['sender_address'] # 发送者邮箱地址
    sender_pass = config['mail']['sneder_password'] #

    # 自己发给自己
    receiver = sender_address

    # 设置总的邮件体对象，对象类型为mixed
    msg_root = MIMEMultipart('mixed')

    # 邮件添加的头尾信息等
    msg_root['From'] = config['mail']['sender_address']
    msg_root['To'] = receiver

    # 邮件的主题，显示在接收邮件的预览页面，以日期为邮件主题
    subject = get_all_funds_today.getYesterday()
    msg_root['subject'] = Header(subject, 'utf-8')

    # 构造文本内容
    text_info = to_send_message()
    text_sub = MIMEText(text_info, 'plain', 'utf-8')
    msg_root.attach(text_sub)


    '''
    # 构造超文本
    url = "https://blog.csdn.net/chinesepython"
    html_info = """
    <p>点击以下链接，你会去向一个更大的世界</p>
    <p><a href="%s">click me</a></p>
    <p>i am very galsses for you</p>
    """% url
    html_sub = MIMEText(html_info, 'html', 'utf-8')
    # 如果不加下边这行代码的话，上边的文本是不会正常显示的，会把超文本的内容当做文本显示
    html_sub["Content-Disposition"] = 'attachment; filename="csdn.html"'   
    # 把构造的内容写到邮件体中
    msg_root.attach(html_sub)

    # 构造图片
    image_file = open(r'D:\python_files\images\test.png', 'rb').read()
    image = MIMEImage(image_file)
    image.add_header('Content-ID', '<image1>')
    # 如果不加下边这行代码的话，会在收件方方面显示乱码的bin文件，下载之后也不能正常打开
    image["Content-Disposition"] = 'attachment; filename="red_people.png"'
    msg_root.attach(image)

    # 构造附件
    txt_file = open(r'D:\python_files\files\hello_world.txt', 'rb').read()
    txt = MIMEText(txt_file, 'base64', 'utf-8')
    txt["Content-Type"] = 'application/octet-stream'
    #以下代码可以重命名附件为hello_world.txt  
    txt.add_header('Content-Disposition', 'attachment', filename='hello_world.txt')
    msg_root.attach(txt)
	'''
    try:
        '''
        sftp_obj = smtplib.SMTP_SSL('smtp.aliyun.com', 465)
        sftp_obj.login(sender_mail, sender_pass)
        sftp_obj.sendmail(sender_mail, to, msg_root.as_string())
        sftp_obj.quit()
        print('sendemail successful!')
        '''
        
        s = smtplib.SMTP()
        s.connect(config['mail']['server'])
        s.login(sender_mail, sender_pass)
        s.sendmail(sender_mail, receiver, msg_root.as_string())
        s.quit()

    except Exception as e:
        logger.error('sendemail failed, the reason: %s', e)


if __name__ == '__main__':
    # 可以是一个列表，支持多个邮件地址同时发送，测试改成自己的邮箱地址
    send_email()







