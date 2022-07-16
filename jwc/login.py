# coding:utf8
import hashlib
import random

import requests
from bs4 import BeautifulSoup

from settings.common import CommonConfig
from settings.spider import JWCCONFIG


class LoginJWC(object):

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password
        self.webfinger = self.get_webfinger()
        self.headers = JWCCONFIG.HEADERS
        self.sess = requests.Session()
        self.sess.headers = self.headers
        self.rnd = self.get_rnd()
        self.code = self.get_code()
        self.username1 = hashlib.md5(username.encode("utf8")).hexdigest()
        self.password1 = hashlib.sha1((username + password).encode("utf8")).hexdigest()
        self.name = ""
        # 是否登录成功
        self.login_status = False

    def get_webfinger(self):
        """
        随机生成浏览器指纹（webfinger）
        :return:
        """
        self.webfinger = "".join([CommonConfig.STRSET[random.randint(0, 35)] for i in range(32)])

        return self.webfinger

    def get_code(self):
        """
        获取浏览器指纹（webfinger）对应的code
        :return:
        """
        if self.webfinger is None:
            self.get_webfinger()
            # raise ValueError("")
        post_data = {
            "webfinger": self.webfinger
        }
        # print(self.sess)
        self.code = self.sess.post(JWCCONFIG.GETCODEURL, data=post_data).text
        return self.code

    def get_rnd(self):
        """
        获取页面必传参数rnd
        :return:
        """
        res = self.sess.get(JWCCONFIG.RNDNURL)
        text = res.text
        soup = BeautifulSoup(text, "html.parser")
        try:
            rnd = soup.find("input", id="rnd")['value'].strip()
            if rnd is None:
                print("没有获取到rnd")
        except Exception:
            # print("")
            return
        self.rnd = rnd
        return rnd

    def login(self):
        """
        登录成功返回 True 失败则返回False
        :return:
        """
        login_data = {
            'UserName': "",  # 如果有这个字段就跳转到重设密码界面了
            'Password': "",
            'type': 'xs',
            'MsgID': "",
            "KeyID": "",
            "rnd": self.rnd,  #
            "userName": self.username,
            "password": self.password,
            "return_EncData": "",
            "code": self.code,  #
            "userName1": self.username1,  #
            "password1": self.password1,  #
            "webfinger": self.webfinger,  #
        }
        res = self.sess.post(JWCCONFIG.LOGINURL, data=login_data)
        #  检测是否登录成功
        soup = BeautifulSoup(res.text, "lxml")
        userinfo_div = soup.find("div", attrs={"class": "main-per-name"})
        if userinfo_div is None:
            self.login_status = False
            return False
        else:
            username = userinfo_div.find("b").text.strip()
            print(username, "登录成功")
            self.name = username
            # 把cookie 缓存起来 sess.cookies
            self.login_status = True
            return True


# 教务管理系统账号
username = ''
# 教务管理系统密码
password = ''

lg = LoginJWC(username=username, password=password)
print(lg.login())
