import json
from licsber.auth.wisedu import get_wisedu_session

#信息门户账号、密码，手机号
EHALL_USER = ''
EHALL_PWD = ''
PHONE_NUMBER = ''

import json
from licsber.auth.wisedu import get_wisedu_session

#信息门户账号、密码，手机号
EHALL_USER = ''
EHALL_PWD = ''
PHONE_NUMBER = ''

LOGIN_URL = 'http://authserver.njit.edu.cn/authserver/login?service=http%3A%2F%2Fehall.njit.edu.cn%2Flogin%3Fservice%3Dhttp%3A%2F%2Fehall.njit.edu.cn%2Fnew%2Findex.html'
GET_URL = 'http://ehallapp.njit.edu.cn/publicapp/sys/lwNjitHealthInfoDailyClock/index.do#/healthClock'
QUERY_URL = 'http://ehallapp.njit.edu.cn/publicapp/sys/lwNjitHealthInfoDailyClock/modules/healthClock/V_LWPUB_JKDK_QUERY.do'
TIME_URL = 'http://ehallapp.njit.edu.cn/publicapp/sys/lwpub/api/getServerTime.do'
SAVE_URL = 'http://ehallapp.njit.edu.cn/publicapp/sys/lwNjitHealthInfoDailyClock/modules/healthClock/T_HEALTH_DAILY_INFO_SAVE.do'

s = get_wisedu_session(LOGIN_URL, EHALL_USER, EHALL_PWD)
s.get(GET_URL)

res = s.post(QUERY_URL)
info_dict = json.loads(res.text)['datas']['V_LWPUB_JKDK_QUERY']['rows'][0]

user_id = info_dict['USER_ID']
user_name = info_dict['USER_NAME']
dept_code = info_dict['DEPT_CODE']
dept_name = info_dict['DEPT_NAME']

res = s.post(TIME_URL)
date = json.loads(res.text)['date']
date = str(date).replace('/','-')

data_am = {
    "USER_ID":user_id,
    "USER_NAME":user_name,
    "DEPT_CODE":dept_code,
    "DEPT_NAME":dept_name,
    "PHONE_NUMBER":PHONE_NUMBER,
    "FILL_TIME":date,
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

res = s.post(SAVE_URL, data=data_pm)
print(res.text)
