"""
    教务管理系统登录接口
"""


class JWCCONFIG():

    PLOGINIP = "202.114.50.129"
    PGRADEIP = "202.114.50.130"

    # 选课url
    COURSEURL = 'http://218.197.102.183/Course'
    # 公选课
    GXKCOURSEURL = COURSEURL + '/gxkxkAdd.do'
    # GXKCOURSEURL = COURSEURL + '/gxkxkAdd'

    LOGINURL = "http://sso.jwc.whut.edu.cn/Certification/login.do"
    RNDNURL = "http://sso.jwc.whut.edu.cn/Certification/toLogin.do"
    GETCODEURL = "http://sso.jwc.whut.edu.cn/Certification/getCode.do"
    GRADEHOMEURL = "http://202.114.50.130/Score/"

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Referer': 'http://sso.jwc.whut.edu.cn/Certification/toLogin.do',
    }
