import json
from licsber.wisedu.get_session import *
from licsber.spider import get_session
from vpn import NJITwebvpn
from webvpn import getVPNUrl

#信息门户账号,密码,手机号 (必填)
EHALL_USER = ''
EHALL_PWD = ''
PHONE_NUMBER = ''

#by2: 住宿信息字段, e.g:张三住北1, by2 = '013'
#[{"id":"001","name":"走读"},{"id":"002","name":"东1"},{"id":"003","name":"东2"},{"id":"004","name":"东3"},{"id":"005","name":"东4"},{"id":"006","name":"东5"},
#{"id":"007","name":"东6"},{"id":"008","name":"东7"},{"id":"009","name":"东8"},{"id":"010","name":"东9"},{"id":"011","name":"东10"},{"id":"012","name":"东11"},
#{"id":"013","name":"北1"},{"id":"014","name":"北2"},{"id":"015","name":"北3"},{"id":"016","name":"北4"},{"id":"017","name":"北5"},{"id":"018","name":"北6"},
#{"id":"019","name":"北7"},{"id":"020","name":"北8"},{"id":"021","name":"北9"},{"id":"022","name":"北10"}]
by2 = ''

s = get_session()
vpn = NJITwebvpn(EHALL_USER,EHALL_PWD)
s = vpn.login()

LOGIN_URL = 'http://authserver.njit.edu.cn/authserver/login?service=http%3A%2F%2Fehall.njit.edu.cn%2Flogin%3Fservice%3Dhttp%3A%2F%2Fehall.njit.edu.cn%2Fnew%2Findex.html'
GET_URL = 'http://ehallapp.njit.edu.cn/publicapp/sys/lwNjitHealthInfoDailyClock/index.do#/healthClock'
QUERY_URL = 'http://ehallapp.njit.edu.cn/publicapp/sys/lwNjitHealthInfoDailyClock/modules/healthClock/V_LWPUB_JKDK_QUERY.do'
TIME_URL = 'http://ehallapp.njit.edu.cn/publicapp/sys/lwpub/api/getServerTime.do'
SAVE_URL = 'http://ehallapp.njit.edu.cn/publicapp/sys/lwNjitHealthInfoDailyClock/modules/healthClock/T_HEALTH_DAILY_INFO_SAVE.do'

URL_DICT = { 'LOGIN_URL': LOGIN_URL, 'GET_URL': GET_URL, 'QUERY_URL': QUERY_URL, 'TIME_URL': TIME_URL, 'SAVE_URL': SAVE_URL }

#套了一层webvpn进行加速，如果不需要就注释掉
#webvpn: 伪内网访问
for k,v in URL_DICT.items():
    URL_DICT[k] = getVPNUrl(v)

s = get_wisedu_session_webvpn(URL_DICT['LOGIN_URL'], EHALL_USER, EHALL_PWD, s)

#公网访问(二选一)
#s = get_wisedu_session(URL_DICT['LOGIN_URL'], EHALL_USER, EHALL_PWD)

s.get(URL_DICT['GET_URL'])

#查询个人信息: 学号, 姓名, 院系编号, 学院名称
res = s.post(URL_DICT['QUERY_URL'])
info_dict = json.loads(res.text)['datas']['V_LWPUB_JKDK_QUERY']['rows'][0]

user_id = info_dict['USER_ID']
user_name = info_dict['USER_NAME']
dept_code = info_dict['DEPT_CODE']
dept_name = info_dict['DEPT_NAME']

#获取服务器时间，可改为本地时间
#时间格式: 2021-09-26 09:51:06
res = s.post(URL_DICT['TIME_URL'])
date = json.loads(res.text)['date']
date = str(date).replace('/','-')

#data_am: 上午提交的信息; data_pm: 下午提交的信息
#BY3字段决定了打卡类型, 001:晨间打卡, 002:晚间打卡
data_am = {
    "USER_ID":user_id,
    "USER_NAME":user_name,
    "DEPT_CODE":dept_code,
    "DEPT_NAME":dept_name,
    "PHONE_NUMBER":PHONE_NUMBER,
    "FILL_TIME":date,
    "BY2": by2
    "BY3": "001",
    "CLOCK_SITUATION":"江苏省南京市江宁区南京工程学院",
    "TODAY_SITUATION":"001",
    "TODAY_VACCINE_CONDITION":"002",
    "TODAY_BODY_CONDITION":"011",
    "TODAY_TEMPERATURE":"002",
    "TODAY_HEALTH_CODE":"001",
    "TODAY_TARRY_CONDITION":"001",
}

data_pm = data_am.copy()
data_pm['BY3'] = '002'

#上午打卡
res = s.post(URL_DICT['SAVE_URL'], data=data_am)
#下午打卡
#res = s.post(URL_DICT['SAVE_URL'], data=data_pm)

print(res.text)
