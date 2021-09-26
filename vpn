import requests

class NJITwebvpn(object):
    '''登录相关操作'''

    def __init__(self, username, password):
        self.session = requests.session()
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/85.0.4183.102 Safari/537.36',
            'Connection': 'keep-alive'
        }                                                                                          # 经测试不添加 header 仍可正常访问
        self.form_data = {
            'auth_type': 'local',
            'username': username,
            'sms_code': '',
            'password': password,
            'captcha': '',
            'needCaptcha': 'false',
            'captcha_id': '',
        }                                                                                          # 貌似只要 post false 就永远不需要验证码hhh
        self.do_login_url = 'https://webvpn.njit.edu.cn/do-login'                                     # 登录 URL

    def login(self):
        res = self.session.post(self.do_login_url, data=self.form_data, headers=self.header).json()
        #print(r)
        if res['success'] == True:
            print("webvpn登录成功")
            return self.session
        else:
            print("webvpn登录失败，请检查学号和密码")
            return None


if __name__  == '__main__':
    try:
        vpn = NJITwebvpn('','')
        session = vpn.login()
        #print(session.cookies)
    except KeyboardInterrupt:
        print('\n操作已取消')
        exit(0)
