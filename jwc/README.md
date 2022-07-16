# 武汉理工大学教务管理系统登录脚本

## 相关依赖

```text
beautifulsoup4==4.11.1
requests==2.28.0
lxml==4.9.0
```

## 使用方法

在`login.py`文件中，配置

```python
# 教务管理系统账号
username = ''
# 教务管理系统密码
password = ''
```

然后调用`login`方法即可实现登录教务管理系统到首页的功能，该方法会返回登录状态`True`or`False`

```python
lg = LoginJWC(username=username, password=password)
lg.login()
```

## 基于LoginJWC类的扩展

通过继承`LoginJWC`类，结合类中的`sess`属性发送网络请求。

下面是结合`LoginJWC`类，实现获取选课系统首页的样例：

```python
class GrabCourses(LoginJWC):
    login_status = False
    xnxq = None
    u_class = None
    filename = None
    # 抢课日志文件
    log_file = None
    write_log_status = False

    def __init__(self, username, password):
        super().__init__(username=username, password=password)
        self.login_status = self.login()
        if self.login_status:
            pass

    def get_grab_course_home(self):
        """
        获取选课列表首页，并读取相关信息，设置选课的学年学期
        :return:
        """
        res = self.sess.get(url=JWCCONFIG.COURSEURL)
        # print(res.text)
        soup = BeautifulSoup(res.text, "lxml")
        header_div = soup.find('div', attrs={'class': 'headerNav'})
        if header_div is not None:
            header_li_list = header_div.find_all('li')
            year_li = header_li_list[0]
            class_li = header_li_list[1]
            self.xnxq = re.findall('[\d]+.[\d]+.[\d]+', year_li.text.strip())[0]
            self.u_class = re.findall('年级：(\d+级)', class_li.text.strip())[0]
            self.write_print_log('获取学年学期：{}\t\t 年级：{}'.format(self.xnxq, self.u_class))
            return True
        else:
            print('选课查询出错')
            return False
```