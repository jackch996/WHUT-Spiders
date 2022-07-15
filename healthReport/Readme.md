# 武汉理工大学健康填报脚本

## 相关依赖

本脚本为Python语言编写
所需依赖如下

```text
APScheduler==3.9.1
requests==2.28.0
```

通过`pip install -r requirements.txt`即可安装

> 只有定时填报的功能用到了`APScheduler`模块，如果不需要通过Python进行定时填报，可以不需要安装。

## 基本使用

在`main.py`文件中，根据个人需求修改如下配置,然后运行程序即可

```python
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
```

## 定时填报

将如下代码取消注释，即可按照24小时的频率进行定时填报

```python
# sched = BlockingScheduler()
# sched.add_job(report_job, 'interval', hours=24)
# sched.start()
```

## 温馨提示

可以找辅导员解绑微信。

## Wx.login()

开发这个微信小程序的程序员对wx.login()接口没有很好的认知。
微信小程序可以使用 wx.login()方法；小程序调用后会获取用户的唯一标识，后端可以根据这个唯一标识进行反爬虫的判断。