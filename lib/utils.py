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
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

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

def doEmailLog(config, succeed):
    msgStr = 'USTC 2020 report success...'
    if not succeed:
        msgStr = 'USTC 2020 report faield...'
    msg = MIMEText(msgStr, 'plain', 'utf-8')
    msg['From'] = 'ustc2020<{}>'.format(config['from_addr'])
    msg['To'] = 'mailing<{}>'.format(config['to_addr'])
    msg['Subject'] = Header('USTC2020', 'utf-8')
    print(msg)

    server = smtplib.SMTP(config['smtp_server'], 25)
    server.set_debuglevel(1)
    server.login(config['from_addr'], config['from_pass'])
    server.sendmail(config['from_addr'],config['to_addr'],msg.as_string())
    server.quit()

def loadConfigFile(path):
    with open(path) as configFile:
        config = json.load(configFile)
        return config

"""
@config: 配置，需要包括'to_phone'参数指定目的号码，'ak'-api access key，'secret'-密钥
@succeed: 
@descr: 阿里云短信通知
"""
def doSMSLog(config, succeed):
    code = 'success'
    if not succeed:
        code = 'failed'
    client = AcsClient(config['ak'], config['secret'], 'cn-hangzhou')
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https') # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', config['to_phone'])
    request.add_query_param('SignName', "USTC2020")
    request.add_query_param('TemplateCode', "SMS_186395017")
    request.add_query_param('TemplateParam', {'code':code})

    response = client.do_action_with_exception(request)
    # python2:  print(response) 
    if response['Message'] == 'OK' and response['Code'] == 'OK':
        return True
    else:
        return False
    print(str(response, encoding = 'utf-8'))