# coding:utf8
import json
from base64 import b64encode, b64decode

import requests

HOST = 'https://zhxg.whut.edu.cn/yqtjwx/'

report_data = {
    "is_in_school": 1,  # 是否在校  1代表是 0代表不是
    "province": "湖北省",  # 省份
    "city": "武汉市",  # 市
    "county": "洪山区",  # 县区
    "street": "文荟街地下通道",  # 街道
}

user_info_list = [
    {
        "sn": "",  # 学号
        "pwd": "",  # 密码
        'report_data': report_data
    },
]


def get_url(path):
    return HOST + '/' + path


# base64
def dict2base64(d):
    return b64encode(json.dumps(d).encode()).decode()


def base64_to_dict(str):
    return json.loads(b64decode(str.encode()).decode())


class WxJKTB():
    sess = None
    sn = None
    pwd = None
    nickname = None
    session_id = None
    report_data = None
    user_base_info = None

    def __init__(self, sn, pwd, report_data, nickname="hello"):
        self.sess = requests.session()
        self.sess.headers[
            'User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36}"
        self.sess.headers['content-type'] = "application/json"
        # 新增： 在header中需要传递encode字段
        self.sess.headers['encode'] = "true"
        self.sn = sn
        self.pwd = pwd
        self.nickname = nickname
        self.user_base_info = {
            "sn": self.sn,
            "idCard": self.pwd,
            "nickname": self.nickname
        }
        self.set_report_data(report_data)

    def set_report_data(self, report_data):

        self.report_data = {
            "diagnosisName": "",
            "relationWithOwn": "",
            "remark": "无",
            "healthInfo": "正常",
            "isDiagnosis": 0,
            "isFever": 0,
            "isInSchool": 0,
            "isLeaveChengdu": 0,
            "isSymptom": "0",
            "temperature": "36.5°C~36.9°C",
            "province": "湖北省",
            "city": "武汉市",
            "county": "洪山区"
        }
        self.report_data.update(**report_data)
        self.report_data["currentAddress"] = self.report_data["province"] + report_data["city"] + report_data[
            "county"] + report_data["street"]

    def get_session_id(self):
        return self.check_bind_user()

    def check_bind_user(self):
        url = get_url('api/login/checkBind')
        post_data = self.user_base_info
        res = self.sess.post(url, data=dict2base64(post_data))
        res_data = base64_to_dict(res.json().get('data'))
        self.session_id = res_data["sessionId"]
        self.sess.headers['Cookie'] = "JSESSIONID={}".format(self.session_id)
        return self.session_id

    def bind_user(self):

        url = get_url('api/login/bindUserInfo')
        post_data = dict2base64(self.user_base_info)
        res_data = self.sess.post(url=url, data=post_data).json()
        status = res_data.get('status')
        msg = res_data.get('message')
        print("登录提示: ", msg)
        if msg == '该学号已被其它微信绑定':
            return status
        if status:
            user_info = base64_to_dict(res_data['data']).get('user')
            if user_info:
                print("获取到用户信息： 姓名:{} \t 班级：{}".format(user_info.get('name'), user_info.get('className')))
            else:
                print("获取用户信息：失败")

        return status

    def report(self):
        url = get_url('./monitorRegister')
        post_data = self.report_data
        post_data = dict2base64(post_data)
        res_data = self.sess.post(url, data=post_data).json()
        if res_data.get("message"):
            print("填报状态: {}".format(res_data["message"]))
        else:
            print("填报状态: 填报完成")

    def cancel_bind_user(self):
        url = get_url('api/login/cancelBind')
        res = self.sess.post(url=url).json()
        res_data = base64_to_dict(res.get('data'))
        print("解绑信息: {}".format(res_data))
        # 关闭请求链接
        self.sess.close()


def make_req(wx_jktb):
    print("====check_bind_user===")
    session_id = wx_jktb.check_bind_user()
    if not session_id:
        print("session_id")
        return
    print("====bind_user===")
    is_bind = wx_jktb.bind_user()
    if not is_bind:
        return
    try:
        print("====report===")
        wx_jktb.report()

    except Exception as e:
        print("msg: err {}".format(e))
        print("====cancel_bind_user===")
        wx_jktb.cancel_bind_user()

    print("====cancel_bind_user===")
    wx_jktb.cancel_bind_user()


def report_job():
    # 执行健康填报任务
    for user_info in user_info_list:
        wx_jktb = WxJKTB(
            **user_info
        )
        make_req(wx_jktb)


report_job()

# 定时填报

# 定义BlockingScheduler
# sched = BlockingScheduler()
# sched.add_job(report_job, 'interval', hours=24)
# sched.start()
