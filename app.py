import lib.autoreport as autoreport
from lib.utils import loadConfigFile, doEmailLog
import schedule
import argparse

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
username = '***'
userpass = '***'
notifyConfig = dict()

def job():
    ret = autoreport.doReport(username, userpass, healthCondition)
    doEmailLog(notifyConfig, ret)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-p','--path', action='store', dest='path', help='config path')
    args = parser.parse_args()
    if args.path is not None:
        config = loadConfigFile(args.path)
        username = config['username']
        userpass = config['userpass']
        healthCondition = config['healthCondition']
        notifyConfig = config

    schedule.every().day.do(job)
    # autoreport.doReport('***', '***', healthCondition)
    while True:
        schedule.run_pending()