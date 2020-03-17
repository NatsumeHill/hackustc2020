# -*- coding: UTF-8 -*-
"""
@author: xiefangkui
@descr:
纯属娱乐。🐶
process：登录测试已经成功，提交数据格式验证完成。是否能够进行提交还未测试。
"""
import requests
from .utils import getLogTime
from bs4 import BeautifulSoup

"""
@username: 用户名
@userpass: 密码
@healthCondition: 健康状况数据
@retutn False-失败 True-成功
"""
def doReport(username, userpass, healthCondition):
    loginUrl = 'https://passport.ustc.edu.cn/login'
    reportUrl = 'http://weixine.ustc.edu.cn/2020/daliy_report'
    loginPayload = {
        'model':'uplogin.jsp',
        'service':'http://weixine.ustc.edu.cn/2020/caslogin',
        'warn':'',
        'showCode':'',
        'username':'***', #账户
        'password':'***', # 密码
        'button':''
    }
    headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}

    s = requests.Session()
    s.headers.update(headers)
    # 从2020跳转登录，以便收集cookie
    r = s.get(loginUrl, params = {'service':'http://weixine.ustc.edu.cn/2020/caslogin'})

    # 调用protal登录
    loginPayload['username'] = username
    loginPayload['password'] = userpass
    r = s.post(loginUrl, data=loginPayload, verify=False)
    if r.status_code == 200 and r.history.__len__() != 0:
        print('::== login ok')
    else:
        print('::== login fail')
        return False

    soup = BeautifulSoup(r.content, features="html.parser")
    # 获取token
    tokenTags = soup.find_all('input', attrs={'type':'hidden','name':'_token'})
    token = ''
    for tokenTag in tokenTags:
        if token != '' and token != tokenTag['value']:
            print('error: can not determin the token')
            return False
        token = tokenTag['value']
    print('::== got token:',token)

    # 上次报告时间
    reportTimeString = getLogTime(soup)
    print('::== last report time:', reportTimeString)

    # 提交报告
    healthCondition['_token']=token
    print('::== report data ]->>\n',healthCondition)
    r = s.post(reportUrl,data=healthCondition) #要提交必须注释！！！！！

    if r.status_code == 200:
        # 本次报告时间
        soup = BeautifulSoup(r.content, features='html.parser')
        currentTimeString = getLogTime(soup)
        print('::== current report time:', currentTimeString)
        if currentTimeString != reportTimeString:
            print('::== report success')
            return True
        else:
            print('::== report warning', r.status_code, r.content[0:6])
            return False
    else:
        print('::== report warning', r.status_code, r.content[0:6])
        return False
