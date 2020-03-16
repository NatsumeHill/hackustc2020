#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
纯属娱乐。🐶
process：登录测试已经成功，提交数据格式验证完成。是否能够进行提交还未测试。
"""
import requests
from bs4 import BeautifulSoup
loginUrl = 'https://passport.ustc.edu.cn/login'
reportUrl = 'http://weixine.ustc.edu.cn/2020/daliy_report'
loginPayload = {
    'model':'uplogin.jsp',
    'service':'http://weixine.ustc.edu.cn/2020/caslogin',
    'warn':'',
    'showCode':'',
    'username':'****', #账户
    'password':'***', # 密码
    'button':''
}
healthCondition = {
    'now_address': '1', #1:内地，2:香港🇭🇰，3:澳门，4:台湾，5:国外
    'gps_now_address': '1', #同上
    'gps_province': '500000', # 省份代码
    'gps_city': '500000', # 城市代码
    'now_detail': '', #
    'body_condition': '1', # 身体状况1:正常，2:疑似，3:确诊，4:其他
    'body_condition_detail': '',
    'now_status': '2', #当前状态1:正常在校，2:正常在家，3:居家留观，4:集中留观，5:住院治疗，6:其他
    'now_status_detail': '',
    'has_fever': '0', #是否发热
    'last_touch_sars': '0', #自寒假开始后，是否接触过确诊或疑似病例的患者
    'last_touch_sars_date': '', #接触时间
    'last_touch_sars_detail': '', 
    'last_touch_hubei': '0', # 是否接触过来自湖北的人员
    'last_touch_hubei_date': '', # 接触时间
    'last_touch_hubei_detail': '',
    'last_cross_hubei': '0', #是否在湖北停留或路过
    'last_cross_hubei_date': '', #时间
    'last_cross_hubei_detail': '',
    'return_dest': '2', # 开学后返校目的地 1:合肥，2:其他
    'return_dest_detail': '苏州研究院', # 具体地点
    'other_detail': '', #其他情况说明
}
headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}

s = requests.Session()
s.headers.update(headers)
r = s.get(loginUrl, params = {'service':'http://weixine.ustc.edu.cn/2020/caslogin'})

r = s.post(loginUrl, data=loginPayload, verify=False)
if r.status_code == 200:
    print('::== login ok')
else:
    print('::== login fail')

soup = BeautifulSoup(r.content, features="html.parser")
# 获取token
tokenTags = soup.find_all('input', attrs={'type':'hidden','name':'_token'})
token = ''
for tokenTag in tokenTags:
    if token != '' and token != tokenTag['value']:
        print('error: can not determin the token')
        exit()
    token = tokenTag['value']
print('::== got token:',token)
healthCondition['_token']=token
print('::== report data ]->>\n',healthCondition)
# r = s.post(reportUrl,data=healthCondition) #要提交必须注释！！！！！
if r.status_code == 200:
    print('::== report success')
else:
    print('::== report warning', r.status_code, r.content)
