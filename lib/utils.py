# -*- coding: UTF-8 -*-
"""
@author: xiefangkui
@descr: 工具包
"""
import re
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

timeStampReg = '(20\d{2}([\.\-/|年月\s]{1,3}\d{1,2}){2}日?(\s?\d{2}:\d{2}(:\d{2})?)?)|(\d{1,2}\s?(分钟|小时|天)前)'

def getLogTime(soup):
    reportTimeLogTag = soup.find_all('span', class_ = 'text-warning')
    reportTimeString = ''
    if reportTimeLogTag is not None and reportTimeLogTag.__len__() == 1:
        reportTimeString = re.search(timeStampReg, reportTimeLogTag[0].parent.text).group()
    return reportTimeString

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def doEmailLog(config):
    msg = MIMEText('USTC 2020 report success...', 'plain', 'utf-8')
    msg['From'] = 'ustc2020<{}>'.format(config['from_addr'])
    msg['To'] = 'mailing<{}>'.format(config['to_addr'])
    msg['Subject'] = Header('USTC2020', 'utf-8')
    print(msg)

    server = smtplib.SMTP(config['smtp_server'], 25)
    server.set_debuglevel(1)
    server.login(config['from_addr'], config['pass'])
    server.sendmail(config['from_addr'],config['to_addr'],msg.as_string())
    server.quit()
